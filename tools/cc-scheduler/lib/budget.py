#!/usr/bin/env python3
"""
Budget tracker for cc-scheduler.

Manages weekly and session-level token budgets to plan Claude Pro usage
across autonomous tasks while reserving capacity for user-directed work.

Budget files stored in .omc/state/:
- weekly-budget.json: Week allocation + actuals by day
- session-budget.json: Current session tracking
- cost-models.json: Learned token estimates per task type
"""

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, date, timedelta
from typing import Optional

# State file locations
BRAIN_ROOT = Path.home() / "brain"
STATE_DIR = BRAIN_ROOT / ".omc" / "state"

WEEKLY_BUDGET_FILE = STATE_DIR / "weekly-budget.json"
SESSION_BUDGET_FILE = STATE_DIR / "session-budget.json"
COST_MODELS_FILE = STATE_DIR / "cost-models.json"


@dataclass
class DailyAllocation:
    """Budget allocation for a single day."""
    planned_percent: float = 0.0
    actual_percent: float = 0.0
    tasks_planned: list = field(default_factory=list)
    tasks_completed: list = field(default_factory=list)


@dataclass
class WeeklyBudget:
    """Weekly budget tracking."""
    week_start: str  # ISO date string (Monday)
    weekly_limit_percent: float = 100.0
    reserve_percent: float = 10.0  # Reserved for user-directed work
    user_directed_used: float = 0.0
    daily_allocations: dict = field(default_factory=dict)  # date_str -> DailyAllocation

    def to_dict(self) -> dict:
        """Convert to serializable dict."""
        return {
            "week_start": self.week_start,
            "weekly_limit_percent": self.weekly_limit_percent,
            "reserve_percent": self.reserve_percent,
            "user_directed_used": self.user_directed_used,
            "daily_allocations": {
                k: asdict(v) if isinstance(v, DailyAllocation) else v
                for k, v in self.daily_allocations.items()
            }
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WeeklyBudget":
        """Create from dict."""
        daily = {}
        for k, v in data.get("daily_allocations", {}).items():
            if isinstance(v, dict):
                daily[k] = DailyAllocation(**v)
            else:
                daily[k] = v
        return cls(
            week_start=data["week_start"],
            weekly_limit_percent=data.get("weekly_limit_percent", 100.0),
            reserve_percent=data.get("reserve_percent", 10.0),
            user_directed_used=data.get("user_directed_used", 0.0),
            daily_allocations=daily
        )


@dataclass
class SessionBudget:
    """Current session budget tracking."""
    session_id: str
    started_at: str
    daily_allocation: float  # Percent allocated for today
    used_percent: float = 0.0
    tasks_executed: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SessionBudget":
        return cls(**data)


class BudgetTracker:
    """
    Manages weekly and session token budgets.

    Default weekly allocation (can be customized in config):
    - Mon-Thu: 15% each = 60%
    - Fri-Sun: 10% each = 30%
    - Reserve: 10%
    """

    DEFAULT_DAILY_ALLOCATION = {
        0: 15.0,  # Monday
        1: 15.0,  # Tuesday
        2: 15.0,  # Wednesday
        3: 15.0,  # Thursday
        4: 10.0,  # Friday
        5: 10.0,  # Saturday
        6: 10.0,  # Sunday
    }

    def __init__(self, config: dict = None):
        self.config = config or {}
        STATE_DIR.mkdir(parents=True, exist_ok=True)

    def _get_week_start(self, d: date = None) -> str:
        """Get Monday of the week containing date d."""
        if d is None:
            d = date.today()
        monday = d - timedelta(days=d.weekday())
        return monday.isoformat()

    def load_weekly_budget(self) -> WeeklyBudget:
        """Load or create weekly budget for current week."""
        current_week = self._get_week_start()

        if WEEKLY_BUDGET_FILE.exists():
            try:
                data = json.loads(WEEKLY_BUDGET_FILE.read_text())
                budget = WeeklyBudget.from_dict(data)

                # Check if it's still the same week
                if budget.week_start == current_week:
                    return budget
                # New week - create fresh budget
            except (json.JSONDecodeError, KeyError):
                pass

        # Create new weekly budget
        budget = WeeklyBudget(week_start=current_week)

        # Initialize daily allocations from config or defaults
        config_daily = self.config.get("budget", {}).get("daily_allocations", {})

        for i in range(7):
            day = date.fromisoformat(current_week) + timedelta(days=i)
            day_str = day.isoformat()

            # Use config allocation or default
            day_name = day.strftime("%A").lower()
            if day_name in config_daily:
                planned = config_daily[day_name]
            else:
                planned = self.DEFAULT_DAILY_ALLOCATION[i]

            budget.daily_allocations[day_str] = DailyAllocation(
                planned_percent=planned
            )

        self.save_weekly_budget(budget)
        return budget

    def save_weekly_budget(self, budget: WeeklyBudget):
        """Save weekly budget to file."""
        WEEKLY_BUDGET_FILE.write_text(
            json.dumps(budget.to_dict(), indent=2)
        )

    def get_today_allocation(self) -> float:
        """Get planned allocation for today."""
        budget = self.load_weekly_budget()
        today = date.today().isoformat()

        if today in budget.daily_allocations:
            alloc = budget.daily_allocations[today]
            if isinstance(alloc, DailyAllocation):
                return alloc.planned_percent
            return alloc.get("planned_percent", 0)
        return 0.0

    def get_remaining_today(self) -> float:
        """Get remaining allocation for today."""
        budget = self.load_weekly_budget()
        today = date.today().isoformat()

        if today in budget.daily_allocations:
            alloc = budget.daily_allocations[today]
            if isinstance(alloc, DailyAllocation):
                return alloc.planned_percent - alloc.actual_percent
            return alloc.get("planned_percent", 0) - alloc.get("actual_percent", 0)
        return 0.0

    def get_remaining_week(self) -> float:
        """Get remaining allocation for the week."""
        budget = self.load_weekly_budget()

        total_used = sum(
            (a.actual_percent if isinstance(a, DailyAllocation) else a.get("actual_percent", 0))
            for a in budget.daily_allocations.values()
        )
        total_used += budget.user_directed_used

        available = budget.weekly_limit_percent - budget.reserve_percent
        return max(0, available - total_used)

    def get_week_summary(self) -> dict:
        """Get summary of weekly budget status."""
        budget = self.load_weekly_budget()
        today = date.today().isoformat()

        total_planned = 0.0
        total_actual = 0.0
        days_remaining = 0

        for day_str, alloc in budget.daily_allocations.items():
            if isinstance(alloc, DailyAllocation):
                planned = alloc.planned_percent
                actual = alloc.actual_percent
            else:
                planned = alloc.get("planned_percent", 0)
                actual = alloc.get("actual_percent", 0)

            total_planned += planned
            total_actual += actual

            if day_str >= today:
                days_remaining += 1

        return {
            "week_start": budget.week_start,
            "total_planned": total_planned,
            "total_used": total_actual,
            "user_directed_used": budget.user_directed_used,
            "reserve": budget.reserve_percent,
            "remaining_week": self.get_remaining_week(),
            "remaining_today": self.get_remaining_today(),
            "days_remaining": days_remaining,
        }

    def record_usage(self, task_name: str, tokens_used: int, percent_used: float):
        """Record token usage for a task."""
        budget = self.load_weekly_budget()
        today = date.today().isoformat()

        if today in budget.daily_allocations:
            alloc = budget.daily_allocations[today]
            if isinstance(alloc, DailyAllocation):
                alloc.actual_percent += percent_used
                alloc.tasks_completed.append({
                    "name": task_name,
                    "tokens": tokens_used,
                    "percent": percent_used,
                    "timestamp": datetime.now().isoformat()
                })
            else:
                alloc["actual_percent"] = alloc.get("actual_percent", 0) + percent_used
                if "tasks_completed" not in alloc:
                    alloc["tasks_completed"] = []
                alloc["tasks_completed"].append({
                    "name": task_name,
                    "tokens": tokens_used,
                    "percent": percent_used,
                    "timestamp": datetime.now().isoformat()
                })

        self.save_weekly_budget(budget)

        # Update cost models
        self._update_cost_model(task_name, tokens_used)

    def record_user_directed(self, percent_used: float):
        """Record usage from user-directed (non-scheduled) work."""
        budget = self.load_weekly_budget()
        budget.user_directed_used += percent_used
        self.save_weekly_budget(budget)

    def _update_cost_model(self, task_name: str, tokens_used: int):
        """Update learned cost estimates using exponential moving average."""
        models = self._load_cost_models()

        # Extract task type from name (e.g., "brain-self-improvement" -> "brain")
        task_type = task_name.split("-")[0] if "-" in task_name else task_name

        if task_type in models:
            # EMA: 0.7 * old + 0.3 * new
            old_estimate = models[task_type]["avg_tokens"]
            models[task_type]["avg_tokens"] = int(0.7 * old_estimate + 0.3 * tokens_used)
            models[task_type]["samples"] += 1
        else:
            models[task_type] = {
                "avg_tokens": tokens_used,
                "samples": 1
            }

        self._save_cost_models(models)

    def _load_cost_models(self) -> dict:
        """Load cost estimation models."""
        if COST_MODELS_FILE.exists():
            try:
                return json.loads(COST_MODELS_FILE.read_text())
            except json.JSONDecodeError:
                pass
        return {}

    def _save_cost_models(self, models: dict):
        """Save cost estimation models."""
        COST_MODELS_FILE.write_text(json.dumps(models, indent=2))

    def get_estimated_cost(self, task_name: str, default: int = 50000) -> int:
        """Get estimated token cost for a task type."""
        models = self._load_cost_models()
        task_type = task_name.split("-")[0] if "-" in task_name else task_name

        if task_type in models:
            return models[task_type]["avg_tokens"]
        return default

    def rebalance_week(self, remaining_tasks: list):
        """
        Rebalance remaining days based on task backlog.

        If we're behind schedule, allocate more to future days.
        If we're ahead, can reduce future allocations.
        """
        budget = self.load_weekly_budget()
        today = date.today()

        # Calculate remaining capacity needed
        total_estimated = sum(
            self.get_estimated_cost(t.get("name", ""), t.get("estimated_tokens", 50000))
            for t in remaining_tasks
        )

        # Get remaining days
        future_days = []
        for day_str in budget.daily_allocations:
            if day_str > today.isoformat():
                future_days.append(day_str)

        if not future_days:
            return  # No future days to rebalance

        # Calculate how much we need per day
        remaining_week = self.get_remaining_week()

        # Simple rebalancing: distribute evenly across remaining days
        per_day = remaining_week / len(future_days)

        for day_str in future_days:
            alloc = budget.daily_allocations[day_str]
            if isinstance(alloc, DailyAllocation):
                alloc.planned_percent = per_day
            else:
                alloc["planned_percent"] = per_day

        self.save_weekly_budget(budget)

    # Session-level tracking

    def start_session(self) -> SessionBudget:
        """Start a new budget tracking session."""
        session = SessionBudget(
            session_id=datetime.now().strftime("session-%Y%m%d-%H%M%S"),
            started_at=datetime.now().isoformat(),
            daily_allocation=self.get_today_allocation()
        )
        SESSION_BUDGET_FILE.write_text(json.dumps(session.to_dict(), indent=2))
        return session

    def load_session(self) -> Optional[SessionBudget]:
        """Load current session if exists."""
        if SESSION_BUDGET_FILE.exists():
            try:
                data = json.loads(SESSION_BUDGET_FILE.read_text())
                return SessionBudget.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                pass
        return None

    def update_session(self, task_name: str, percent_used: float):
        """Update current session tracking."""
        session = self.load_session()
        if session:
            session.used_percent += percent_used
            session.tasks_executed.append({
                "name": task_name,
                "percent": percent_used,
                "timestamp": datetime.now().isoformat()
            })
            SESSION_BUDGET_FILE.write_text(json.dumps(session.to_dict(), indent=2))

    def check_session_budget(self, estimated_percent: float) -> bool:
        """Check if a task fits in the session budget."""
        session = self.load_session()
        if not session:
            return True  # No session tracking, allow

        remaining = session.daily_allocation - session.used_percent
        return estimated_percent <= remaining


def format_budget_status(tracker: BudgetTracker) -> str:
    """Format budget status for display."""
    summary = tracker.get_week_summary()

    lines = [
        f"Week of {summary['week_start']}:",
        f"  Today remaining: {summary['remaining_today']:.1f}%",
        f"  Week remaining:  {summary['remaining_week']:.1f}%",
        f"  Used this week:  {summary['total_used']:.1f}%",
        f"  User-directed:   {summary['user_directed_used']:.1f}%",
        f"  Reserve:         {summary['reserve']:.1f}%",
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    tracker = BudgetTracker()
    print(format_budget_status(tracker))
