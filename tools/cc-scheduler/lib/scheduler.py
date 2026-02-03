#!/usr/bin/env python3
"""
Smart scheduler for cc-scheduler.

Handles:
- Priority scoring with 5 factors
- Session and week budget planning
- Time window enforcement (autonomous/briefing/reserved phases)
- Confidence-based routing
"""

from dataclasses import dataclass
from datetime import datetime, time, date
from typing import Optional, List, Tuple
from pathlib import Path

from .tasks import Task
from .budget import BudgetTracker
from .capacity import Capacity


@dataclass
class ScheduleConfig:
    """Schedule configuration."""
    # Time windows (24h format)
    autonomous_start: time = time(8, 0)   # 8 AM - start autonomous work
    autonomous_end: time = time(14, 0)    # 2 PM - end autonomous
    briefing_time: time = time(14, 0)     # 2 PM - briefing window
    reserved_start: time = time(20, 0)    # 8 PM - user's peak hours
    reserved_end: time = time(8, 0)       # 8 AM - end reserved

    # Budget allocation per phase (percent of daily)
    budget_autonomous: float = 0.80
    budget_briefing: float = 0.08
    budget_buffer: float = 0.12

    # Priority weights
    weight_user_priority: float = 100.0
    weight_urgency: float = 50.0
    weight_cost_efficiency: float = 30.0
    weight_project_boost: float = 20.0
    weight_dependency_penalty: float = 10.0

    # Confidence thresholds
    confidence_auto_proceed: int = 90
    confidence_review_threshold: int = 70
    confidence_question_threshold: int = 50

    @classmethod
    def from_dict(cls, data: dict) -> "ScheduleConfig":
        """Create config from dict (loaded from YAML)."""
        schedule = data.get("schedule", {})
        budget = data.get("budget", {})
        weights = data.get("weights", {})
        confidence = data.get("confidence", {})

        def parse_time(s: str) -> time:
            if not s:
                return None
            parts = s.split(":")
            return time(int(parts[0]), int(parts[1]))

        config = cls()

        if "autonomous_start" in schedule:
            config.autonomous_start = parse_time(schedule["autonomous_start"])
        if "autonomous_end" in schedule:
            config.autonomous_end = parse_time(schedule["autonomous_end"])
        if "briefing_time" in schedule:
            config.briefing_time = parse_time(schedule["briefing_time"])
        if "reserved_start" in schedule:
            config.reserved_start = parse_time(schedule["reserved_start"])
        if "reserved_end" in schedule:
            config.reserved_end = parse_time(schedule["reserved_end"])

        if "autonomous" in budget:
            config.budget_autonomous = budget["autonomous"]
        if "briefing" in budget:
            config.budget_briefing = budget["briefing"]
        if "buffer" in budget:
            config.budget_buffer = budget["buffer"]

        if "user_priority" in weights:
            config.weight_user_priority = weights["user_priority"]
        if "urgency" in weights:
            config.weight_urgency = weights["urgency"]
        if "cost_efficiency" in weights:
            config.weight_cost_efficiency = weights["cost_efficiency"]
        if "project_boost" in weights:
            config.weight_project_boost = weights["project_boost"]
        if "dependency_penalty" in weights:
            config.weight_dependency_penalty = weights["dependency_penalty"]

        if "auto_proceed" in confidence:
            config.confidence_auto_proceed = confidence["auto_proceed"]
        if "review_threshold" in confidence:
            config.confidence_review_threshold = confidence["review_threshold"]
        if "question_threshold" in confidence:
            config.confidence_question_threshold = confidence["question_threshold"]

        return config


class Scheduler:
    """
    Smart task scheduler with priority scoring and budget planning.
    """

    def __init__(self, config: ScheduleConfig = None, budget_tracker: BudgetTracker = None):
        self.config = config or ScheduleConfig()
        self.budget = budget_tracker or BudgetTracker()
        self.project_boosts = {}  # project_name -> boost value

    def set_project_boosts(self, boosts: dict):
        """Set project priority boosts from config."""
        self.project_boosts = boosts

    # =========================================================================
    # Time Window Management
    # =========================================================================

    def get_current_phase(self, now: datetime = None) -> str:
        """
        Get current schedule phase.

        Phases:
        - autonomous: 8 AM - 2 PM (when user is sleeping/away)
        - briefing: 2 PM - 3 PM (user wakes, review results)
        - buffer: 3 PM - 8 PM (light tasks, user may be active)
        - reserved: 8 PM - 8 AM (user's peak hours, no autonomous)
        """
        if now is None:
            now = datetime.now()

        current = now.time()

        # Check autonomous window (8 AM - 2 PM)
        if self.config.autonomous_start <= current < self.config.autonomous_end:
            return "autonomous"

        # Check briefing window (2 PM - 3 PM typically)
        briefing_end = time(
            self.config.briefing_time.hour + 1,
            self.config.briefing_time.minute
        )
        if self.config.briefing_time <= current < briefing_end:
            return "briefing"

        # Check reserved window (8 PM - 8 AM)
        # This wraps around midnight
        if current >= self.config.reserved_start or current < self.config.reserved_end:
            return "reserved"

        # Default to buffer
        return "buffer"

    def should_run_now(self, phase: str = None) -> Tuple[bool, str]:
        """
        Check if autonomous tasks should run now.

        Returns (should_run, reason).
        """
        if phase is None:
            phase = self.get_current_phase()

        if phase == "autonomous":
            return True, "Autonomous window active"
        elif phase == "briefing":
            return False, "Briefing window - review results instead"
        elif phase == "buffer":
            return True, "Buffer window - light tasks only"
        else:  # reserved
            return False, "Reserved for user - no autonomous tasks"

    def get_phase_budget(self, phase: str) -> float:
        """Get budget allocation for a phase as fraction of daily."""
        if phase == "autonomous":
            return self.config.budget_autonomous
        elif phase == "briefing":
            return self.config.budget_briefing
        else:
            return self.config.budget_buffer

    # =========================================================================
    # Priority Scoring
    # =========================================================================

    def score_task(self, task: Task, capacity: Capacity = None) -> float:
        """
        Calculate priority score for a task.

        Factors (weighted):
        1. User-assigned priority (1-10 scale, lower = higher priority)
        2. Urgency (deadline proximity)
        3. Cost efficiency (tokens vs value)
        4. Project boost (from config)
        5. Dependency penalty (blocked tasks score lower)

        Returns score (higher = run sooner).
        """
        score = 0.0

        # 1. User priority (inverted: priority 1 -> score 100, priority 10 -> score 10)
        priority_score = (11 - task.priority) * 10
        score += priority_score * (self.config.weight_user_priority / 100)

        # 2. Urgency (deadline proximity)
        if task.deadline:
            days_until = (task.deadline - datetime.now()).days
            if days_until <= 0:
                urgency_score = 100  # Overdue!
            elif days_until <= 1:
                urgency_score = 90
            elif days_until <= 3:
                urgency_score = 70
            elif days_until <= 7:
                urgency_score = 50
            else:
                urgency_score = 20
        else:
            urgency_score = 30  # No deadline = medium urgency
        score += urgency_score * (self.config.weight_urgency / 100)

        # 3. Cost efficiency (prefer smaller tasks when capacity is low)
        if capacity and capacity.available_percent < 30:
            # Boost smaller tasks when capacity is tight
            if task.estimated_tokens < 30000:
                efficiency_score = 80
            elif task.estimated_tokens < 60000:
                efficiency_score = 50
            else:
                efficiency_score = 20
        else:
            efficiency_score = 50  # Neutral when capacity is fine
        score += efficiency_score * (self.config.weight_cost_efficiency / 100)

        # 4. Project boost
        project = getattr(task, 'project', None) or task.tags[0] if task.tags else None
        if project and project in self.project_boosts:
            score += self.project_boosts[project] * (self.config.weight_project_boost / 100)

        # 5. Dependency penalty
        if task.depends_on:
            # Penalize blocked tasks
            score -= len(task.depends_on) * 10 * (self.config.weight_dependency_penalty / 100)

        return max(0, score)

    def rank_tasks(self, tasks: List[Task], capacity: Capacity = None) -> List[Tuple[Task, float]]:
        """Rank tasks by priority score."""
        scored = [(t, self.score_task(t, capacity)) for t in tasks]
        return sorted(scored, key=lambda x: x[1], reverse=True)

    def select_next_task(self, tasks: List[Task], capacity: Capacity = None) -> Optional[Task]:
        """Select the highest-priority runnable task."""
        if not tasks:
            return None

        ranked = self.rank_tasks(tasks, capacity)

        for task, score in ranked:
            if task.is_runnable:
                return task

        return None

    # =========================================================================
    # Session Planning
    # =========================================================================

    def plan_session(
        self,
        tasks: List[Task],
        capacity: Capacity,
        phase: str = None
    ) -> List[Task]:
        """
        Plan which tasks to run in this session.

        Considers:
        - Available capacity (from API)
        - Daily budget allocation
        - Phase budget (autonomous gets more than buffer)
        - Task priority scores
        """
        if phase is None:
            phase = self.get_current_phase()

        # Get budget constraints
        daily_remaining = self.budget.get_remaining_today()
        phase_budget = self.get_phase_budget(phase) * daily_remaining

        # Convert to tokens (rough estimate: 1% = 5000 tokens)
        available_tokens = min(
            capacity.available_percent * 5000,
            phase_budget * 5000
        )

        # Rank tasks
        ranked = self.rank_tasks(tasks, capacity)

        # Select tasks that fit
        selected = []
        tokens_planned = 0

        for task, score in ranked:
            if not task.is_runnable:
                continue

            if tokens_planned + task.estimated_tokens <= available_tokens:
                selected.append(task)
                tokens_planned += task.estimated_tokens

        return selected

    def plan_week(self, tasks: List[Task]) -> dict:
        """
        Plan task distribution across the week.

        Returns dict of {date_str: [task_names]}.
        """
        from datetime import timedelta

        # Get weekly budget
        weekly = self.budget.load_weekly_budget()
        today = date.today()

        # Rank all tasks
        ranked = self.rank_tasks(tasks)

        plan = {}
        task_queue = list(ranked)  # Copy

        for day_offset in range(7):
            day = today + timedelta(days=day_offset)
            day_str = day.isoformat()

            if day_str not in weekly.daily_allocations:
                continue

            alloc = weekly.daily_allocations[day_str]
            if hasattr(alloc, 'planned_percent'):
                day_budget = alloc.planned_percent * 5000  # tokens
            else:
                day_budget = alloc.get('planned_percent', 0) * 5000

            day_tasks = []
            day_tokens = 0

            # Assign tasks to this day
            remaining = []
            for task, score in task_queue:
                if day_tokens + task.estimated_tokens <= day_budget:
                    day_tasks.append(task.name)
                    day_tokens += task.estimated_tokens
                else:
                    remaining.append((task, score))

            plan[day_str] = day_tasks
            task_queue = remaining

        return plan

    # =========================================================================
    # Confidence Routing
    # =========================================================================

    def route_by_confidence(self, task: Task, confidence: int) -> str:
        """
        Determine action based on confidence level.

        Returns:
        - "proceed": Execute autonomously
        - "review": Execute but flag for review
        - "question": Ask user before proceeding
        - "skip": Don't execute
        """
        if confidence >= self.config.confidence_auto_proceed:
            return "proceed"
        elif confidence >= self.config.confidence_review_threshold:
            return "review"
        elif confidence >= self.config.confidence_question_threshold:
            return "question"
        else:
            return "skip"

    def check_budget(self, task: Task) -> Tuple[bool, str]:
        """
        Check if task fits in current budget.

        Returns (fits, reason).
        """
        # Estimate percent cost (rough: 50k tokens = 10%)
        estimated_percent = task.estimated_tokens / 5000

        # Check session budget
        if not self.budget.check_session_budget(estimated_percent):
            return False, "Exceeds session budget"

        # Check daily remaining
        remaining = self.budget.get_remaining_today()
        if estimated_percent > remaining:
            return False, f"Exceeds daily budget ({remaining:.1f}% remaining)"

        # Check weekly remaining
        week_remaining = self.budget.get_remaining_week()
        if estimated_percent > week_remaining:
            return False, f"Exceeds weekly budget ({week_remaining:.1f}% remaining)"

        return True, "Within budget"


def format_schedule_status(scheduler: Scheduler) -> str:
    """Format schedule status for display."""
    phase = scheduler.get_current_phase()
    can_run, reason = scheduler.should_run_now(phase)

    lines = [
        f"Current phase: {phase}",
        f"Can run tasks: {'Yes' if can_run else 'No'} ({reason})",
        f"",
        f"Schedule windows:",
        f"  Autonomous: {scheduler.config.autonomous_start.strftime('%H:%M')} - {scheduler.config.autonomous_end.strftime('%H:%M')}",
        f"  Briefing:   {scheduler.config.briefing_time.strftime('%H:%M')}",
        f"  Reserved:   {scheduler.config.reserved_start.strftime('%H:%M')} - {scheduler.config.reserved_end.strftime('%H:%M')}",
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    scheduler = Scheduler()
    print(format_schedule_status(scheduler))
