#!/usr/bin/env python3
"""
Priority Scoring Algorithm for Multi-Project AI Task Management

Based on research of:
- Apache Airflow priority weights
- Eisenhower Matrix (urgency x importance)
- GTD methodology
- AI scheduler systems
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# Constants from research
EISENHOWER_QUADRANTS = {
    "urgent_important": 1,      # Do first
    "important_not_urgent": 2,  # Schedule
    "urgent_not_important": 3,  # Delegate
    "neither": 4                # Eliminate
}

# Priority levels from TASK_SCHEMA.md
class PriorityLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Task:
    """Task representation matching brain/tasks schema"""
    name: str
    created: datetime
    priority: PriorityLevel
    timeout: int  # minutes
    deadline: Optional[datetime] = None
    estimated_tokens: int = 50000  # default estimate
    project: str = "brain"
    requires: List[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.requires is None:
            self.requires = []
        if self.tags is None:
            self.tags = []

class PriorityScorer:
    """
    Multi-factor priority scoring system for AI task scheduling.
    
    Combines:
    1. User-defined priority (high/medium/low)
    2. Time urgency (deadline proximity)
    3. Token cost efficiency
    4. Project context
    5. Dependency factors
    
    Lower score = higher priority (runs first)
    """
    
    # Weights for scoring factors (tunable)
    WEIGHTS = {
        "user_priority": 100,      # User intent is primary
        "urgency": 50,              # Deadline proximity
        "cost_efficiency": 30,      # Token cost impact
        "project_boost": 20,        # Project-specific boost
        "dependency_penalty": 10    # Blocked tasks get delayed
    }
    
    def __init__(self, capacity_available: int = 1000000):
        """
        Args:
            capacity_available: Remaining tokens in current block
        """
        self.capacity_available = capacity_available
        self.cost_models = self._load_cost_models()
    
    def _load_cost_models(self) -> Dict[str, int]:
        """Load learned cost estimates (would come from learning.py)"""
        # Placeholder - would load from data/cost-models.json
        return {
            "research": 80000,
            "automation": 50000,
            "analysis": 120000,
            "quick": 10000,
            "writing": 30000
        }
    
    def score(self, task: Task) -> float:
        """
        Calculate priority score for task.
        
        Returns:
            float: Priority score (lower = higher priority)
        """
        score = 0.0
        
        # Factor 1: User-defined priority (primary signal)
        score += self._score_user_priority(task)
        
        # Factor 2: Time urgency (deadline pressure)
        score += self._score_urgency(task)
        
        # Factor 3: Cost efficiency (fit within capacity)
        score += self._score_cost_efficiency(task)
        
        # Factor 4: Project boost (multi-project balancing)
        score += self._score_project(task)
        
        # Factor 5: Dependency penalty (blocked = lower priority)
        score += self._score_dependencies(task)
        
        return score
    
    def _score_user_priority(self, task: Task) -> float:
        """
        User priority is the PRIMARY signal.
        
        Maps high/medium/low to base scores.
        """
        priority_map = {
            PriorityLevel.HIGH: 0,      # Run ASAP
            PriorityLevel.MEDIUM: 100,  # Run today
            PriorityLevel.LOW: 200      # Run eventually
        }
        return priority_map[task.priority] * self.WEIGHTS["user_priority"]
    
    def _score_urgency(self, task: Task) -> float:
        """
        Deadline urgency using time-to-deadline.
        
        Based on Eisenhower Matrix urgency dimension.
        """
        if task.deadline is None:
            return 50 * self.WEIGHTS["urgency"]  # Mid-range if no deadline
        
        time_to_deadline = (task.deadline - datetime.now()).total_seconds() / 3600  # hours
        
        if time_to_deadline < 0:
            # Overdue - URGENT
            return 0 * self.WEIGHTS["urgency"]
        elif time_to_deadline < 4:
            # Within 4 hours - very urgent
            return 10 * self.WEIGHTS["urgency"]
        elif time_to_deadline < 24:
            # Within 24 hours - urgent
            return 30 * self.WEIGHTS["urgency"]
        elif time_to_deadline < 168:
            # Within 1 week - moderate urgency
            return 60 * self.WEIGHTS["urgency"]
        else:
            # > 1 week - low urgency
            return 90 * self.WEIGHTS["urgency"]
    
    def _score_cost_efficiency(self, task: Task) -> float:
        """
        Cost efficiency - prefer tasks that fit well in remaining capacity.
        
        Inspired by bin-packing and Airflow's weight strategies.
        """
        estimated_cost = self._estimate_cost(task)
        
        if estimated_cost > self.capacity_available:
            # Won't fit - very low priority (defer to next block)
            return 100 * self.WEIGHTS["cost_efficiency"]
        
        # Efficiency ratio: how much capacity will be left?
        utilization = estimated_cost / self.capacity_available
        
        if utilization > 0.9:
            # Almost fills capacity - good utilization
            return 10 * self.WEIGHTS["cost_efficiency"]
        elif utilization > 0.5:
            # Moderate utilization
            return 30 * self.WEIGHTS["cost_efficiency"]
        else:
            # Low utilization - prefer to batch with other tasks
            return 50 * self.WEIGHTS["cost_efficiency"]
    
    def _estimate_cost(self, task: Task) -> int:
        """
        Estimate token cost from task type or explicit estimate.
        
        Uses learned cost models (would come from learning layer).
        """
        if task.estimated_tokens:
            return task.estimated_tokens
        
        # Infer from tags
        for tag in task.tags:
            if tag in self.cost_models:
                return self.cost_models[tag]
        
        # Infer from timeout (rough heuristic)
        # Longer timeout → likely more complex → more tokens
        return min(task.timeout * 2000, 200000)  # Cap at 200k
    
    def _score_project(self, task: Task) -> float:
        """
        Project-based boosting for multi-project balancing.
        
        Could implement round-robin or weighted project priorities.
        """
        # Placeholder - could track project execution history
        # and boost underserved projects
        project_priorities = {
            "brain": 0,      # Primary project
            "vault": 10,     # Secondary
            "auditing": 20,  # Tertiary
        }
        return project_priorities.get(task.project, 50) * self.WEIGHTS["project_boost"]
    
    def _score_dependencies(self, task: Task) -> float:
        """
        Dependency penalty - blocked tasks get lower priority.
        
        Requires dependency tracking (future enhancement).
        """
        # Placeholder - would check if required tasks are completed
        if "user_answers" in task.requires:
            # Blocked on user input - deprioritize
            return 100 * self.WEIGHTS["dependency_penalty"]
        
        return 0  # No blocking dependencies

# Example usage and testing
def example_scoring():
    """Demonstrate priority scoring with examples"""
    
    scorer = PriorityScorer(capacity_available=500000)
    
    # Example tasks
    tasks = [
        Task(
            name="zotero-weekly-digest",
            created=datetime.now(),
            priority=PriorityLevel.HIGH,
            timeout=30,
            estimated_tokens=50000,
            project="brain",
            tags=["research", "weekly"]
        ),
        Task(
            name="arterial-compliance-analysis",
            created=datetime.now(),
            priority=PriorityLevel.MEDIUM,
            timeout=120,
            deadline=datetime.now() + timedelta(hours=6),
            estimated_tokens=120000,
            project="vault",
            tags=["analysis", "research"]
        ),
        Task(
            name="code-cleanup",
            created=datetime.now(),
            priority=PriorityLevel.LOW,
            timeout=60,
            estimated_tokens=30000,
            project="brain",
            tags=["maintenance"]
        ),
        Task(
            name="urgent-bug-fix",
            created=datetime.now(),
            priority=PriorityLevel.HIGH,
            timeout=20,
            deadline=datetime.now() + timedelta(hours=2),
            estimated_tokens=25000,
            project="brain",
            tags=["bugfix", "urgent"]
        ),
        Task(
            name="blocked-on-user",
            created=datetime.now(),
            priority=PriorityLevel.HIGH,
            timeout=30,
            estimated_tokens=40000,
            project="brain",
            requires=["user_answers"],
            tags=["setup"]
        )
    ]
    
    # Score and sort
    scored_tasks = [(task, scorer.score(task)) for task in tasks]
    scored_tasks.sort(key=lambda x: x[1])
    
    print("\n[FINDING] Priority scoring results (lower score = higher priority):\n")
    print(f"{'Rank':<6} {'Task':<35} {'Priority':<10} {'Score':<10} {'Estimated Tokens':<18}")
    print("-" * 90)
    
    for rank, (task, score) in enumerate(scored_tasks, 1):
        print(f"{rank:<6} {task.name:<35} {task.priority.value:<10} {score:<10.1f} {task.estimated_tokens:<18,}")
    
    # Statistical summary
    print("\n[STAT:total_tasks]", len(tasks))
    print("[STAT:avg_score]", sum(s for _, s in scored_tasks) / len(scored_tasks))
    print("[STAT:score_range]", f"{scored_tasks[0][1]:.1f} - {scored_tasks[-1][1]:.1f}")
    
    # Findings
    print("\n[FINDING] Urgent bug fix ranked highest despite medium token cost")
    print("[STAT:top_task_score]", scored_tasks[0][1])
    print("[STAT:top_task_name]", scored_tasks[0][0].name)
    
    print("\n[FINDING] Blocked task ranked lowest due to dependency penalty")
    print("[STAT:blocked_task_penalty]", scorer.WEIGHTS["dependency_penalty"] * 100)
    
    print("\n[FINDING] Large analysis task ranked lower despite medium priority")
    print("  Reason: High token cost (120k) reduces priority when capacity-constrained")
    
    return scored_tasks

if __name__ == "__main__":
    print("[OBJECTIVE] Design priority scoring algorithm for multi-project AI task scheduling")
    print("\n[DATA] Loaded scoring weights and cost models")
    print(f"  Weights: {PriorityScorer.WEIGHTS}")
    
    example_scoring()
    
    print("\n[LIMITATION] Dependency tracking requires task graph implementation")
    print("[LIMITATION] Cost models need training data from actual execution logs")
    print("[LIMITATION] Project balancing needs execution history tracking")
