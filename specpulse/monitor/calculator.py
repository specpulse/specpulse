"""
Progress Calculation Engine

This module provides the ProgressCalculator class for calculating progress percentages,
trend analysis, performance metrics, and progress predictions.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import statistics
import math

from .models import TaskInfo, ProgressData, TaskHistory, TaskState


class ProgressCalculator:
    """Calculates progress metrics and analytics for task monitoring."""

    def __init__(self):
        """Initialize progress calculator."""
        self._performance_cache: Dict[str, List[float]] = {}
        self._trend_cache: Dict[str, List[float]] = {}

    def calculate_progress(self, tasks: List[TaskInfo], feature_id: Optional[str] = None) -> ProgressData:
        """Calculate overall progress from a list of tasks."""
        if not tasks:
            return ProgressData(
                total_tasks=0,
                completed_tasks=0,
                in_progress_tasks=0,
                blocked_tasks=0,
                pending_tasks=0,
                percentage=0.0,
                last_updated=datetime.now(),
                feature_id=feature_id,
            )

        # Count tasks by state
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.state == TaskState.COMPLETED)
        in_progress_tasks = sum(1 for task in tasks if task.state == TaskState.IN_PROGRESS)
        blocked_tasks = sum(1 for task in tasks if task.state == TaskState.BLOCKED)
        pending_tasks = sum(1 for task in tasks if task.state == TaskState.PENDING)

        # Calculate percentage with edge case handling
        percentage = 0.0
        if total_tasks > 0:
            if blocked_tasks > 0:
                # Penalize progress for blocked tasks
                available_tasks = total_tasks - blocked_tasks
                if available_tasks > 0:
                    percentage = (completed_tasks / total_tasks) * 100
                else:
                    percentage = 0.0
            else:
                percentage = (completed_tasks / total_tasks) * 100

        return ProgressData(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            in_progress_tasks=in_progress_tasks,
            blocked_tasks=blocked_tasks,
            pending_tasks=pending_tasks,
            percentage=round(percentage, 1),
            last_updated=datetime.now(),
            feature_id=feature_id,
        )

    def calculate_weighted_progress(self, tasks: List[TaskInfo], feature_id: Optional[str] = None) -> ProgressData:
        """Calculate weighted progress based on task estimates."""
        if not tasks:
            return self.calculate_progress(tasks, feature_id)

        # Group tasks by state and calculate weights
        state_weights = {
            TaskState.COMPLETED: 1.0,
            TaskState.IN_PROGRESS: 0.5,
            TaskState.PENDING: 0.0,
            TaskState.BLOCKED: 0.0,
        }

        total_weight = 0.0
        completed_weight = 0.0

        for task in tasks:
            # Use estimated hours if available, otherwise default to 1 hour
            task_weight = task.estimated_hours or 1.0
            total_weight += task_weight

            if task.state == TaskState.COMPLETED:
                completed_weight += task_weight
            elif task.state == TaskState.IN_PROGRESS:
                completed_weight += task_weight * 0.5  # Half credit for in-progress

        # Calculate weighted percentage
        percentage = (completed_weight / total_weight * 100) if total_weight > 0 else 0.0

        # Count tasks by state for other metrics
        completed_tasks = sum(1 for task in tasks if task.state == TaskState.COMPLETED)
        in_progress_tasks = sum(1 for task in tasks if task.state == TaskState.IN_PROGRESS)
        blocked_tasks = sum(1 for task in tasks if task.state == TaskState.BLOCKED)
        pending_tasks = sum(1 for task in tasks if task.state == TaskState.PENDING)

        return ProgressData(
            total_tasks=len(tasks),
            completed_tasks=completed_tasks,
            in_progress_tasks=in_progress_tasks,
            blocked_tasks=blocked_tasks,
            pending_tasks=pending_tasks,
            percentage=round(percentage, 1),
            last_updated=datetime.now(),
            feature_id=feature_id,
        )

    def analyze_progress_trend(self, history: List[TaskHistory], days: int = 7) -> Dict[str, any]:
        """Analyze progress trends from historical data."""
        if not history:
            return {
                "trend": "stable",
                "rate": 0.0,
                "daily_completion": [],
                "prediction": None,
                "confidence": 0.0,
            }

        # Filter history to specified time period
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_history = [
            entry for entry in history
            if entry.timestamp > cutoff_date and entry.new_state == TaskState.COMPLETED
        ]

        if not recent_history:
            return {
                "trend": "no_data",
                "rate": 0.0,
                "daily_completion": [],
                "prediction": None,
                "confidence": 0.0,
            }

        # Group completions by day
        daily_completions = {}
        for entry in recent_history:
            day_key = entry.timestamp.date().isoformat()
            daily_completions[day_key] = daily_completions.get(day_key, 0) + 1

        # Create complete daily list for the period
        daily_list = []
        current_date = datetime.now().date()
        for i in range(days):
            date_key = (current_date - timedelta(days=i)).isoformat()
            daily_list.append(daily_completions.get(date_key, 0))

        daily_list.reverse()  # Oldest to newest

        # Calculate completion rate
        total_completed = len(recent_history)
        rate = total_completed / days

        # Determine trend
        if len(daily_list) >= 3:
            recent_avg = statistics.mean(daily_list[-3:])
            earlier_avg = statistics.mean(daily_list[:-3]) if len(daily_list) > 3 else recent_avg

            if recent_avg > earlier_avg * 1.2:
                trend = "accelerating"
            elif recent_avg < earlier_avg * 0.8:
                trend = "decelerating"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        # Predict completion time
        prediction = self._predict_completion_time(recent_history, rate)

        # Calculate confidence based on data consistency
        confidence = self._calculate_prediction_confidence(daily_list)

        return {
            "trend": trend,
            "rate": round(rate, 2),
            "daily_completion": daily_list,
            "prediction": prediction,
            "confidence": confidence,
        }

    def _predict_completion_time(self, history: List[TaskHistory], current_rate: float) -> Optional[Dict[str, any]]:
        """Predict time to complete remaining tasks."""
        if current_rate <= 0:
            return None

        # Calculate remaining tasks (simplified - assumes current feature)
        remaining_tasks = max(0, 10)  # This would come from current project state

        if remaining_tasks == 0:
            return {"days": 0, "date": datetime.now().date().isoformat()}

        predicted_days = math.ceil(remaining_tasks / current_rate)
        completion_date = (datetime.now() + timedelta(days=predicted_days)).date()

        return {
            "days": predicted_days,
            "date": completion_date.isoformat(),
            "confidence": "low" if predicted_days > 30 else "medium" if predicted_days > 7 else "high",
        }

    def _calculate_prediction_confidence(self, daily_values: List[float]) -> float:
        """Calculate confidence score for predictions based on data variance."""
        if len(daily_values) < 3:
            return 0.0

        try:
            mean_val = statistics.mean(daily_values)
            if mean_val == 0:
                return 0.0

            stdev = statistics.stdev(daily_values)
            coefficient_of_variation = stdev / mean_val

            # Convert to confidence score (lower variance = higher confidence)
            confidence = max(0.0, 1.0 - coefficient_of_variation)
            return round(confidence, 2)
        except statistics.StatisticsError:
            return 0.0

    def calculate_performance_metrics(self, tasks: List[TaskInfo], history: List[TaskHistory]) -> Dict[str, any]:
        """Calculate performance metrics for tasks."""
        metrics = {
            "average_execution_time": None,
            "total_execution_time": 0.0,
            "completed_with_time": 0,
            "cycle_time_stats": {},
            "throughput": {},
            "bottleneck_tasks": [],
        }

        # Calculate execution time metrics
        execution_times = [
            task.execution_time for task in tasks
            if task.execution_time is not None and task.state == TaskState.COMPLETED
        ]

        if execution_times:
            metrics["average_execution_time"] = round(statistics.mean(execution_times), 2)
            metrics["total_execution_time"] = sum(execution_times)
            metrics["completed_with_time"] = len(execution_times)

            # Calculate cycle time statistics
            metrics["cycle_time_stats"] = {
                "min": round(min(execution_times), 2),
                "max": round(max(execution_times), 2),
                "median": round(statistics.median(execution_times), 2),
                "std_dev": round(statistics.stdev(execution_times), 2) if len(execution_times) > 1 else 0.0,
            }

        # Calculate throughput metrics
        completed_tasks = [task for task in tasks if task.state == TaskState.COMPLETED]
        if completed_tasks:
            # Calculate task age in days
            now = datetime.now()
            task_ages = []
            for task in completed_tasks:
                if task.last_updated:
                    age_days = (now - task.last_updated).days
                    task_ages.append(age_days)

            if task_ages:
                # Calculate throughput as tasks completed per day
                oldest_task = min(task_ages)
                throughput_rate = len(completed_tasks) / max(oldest_task, 1)
                metrics["throughput"] = {
                    "tasks_per_day": round(throughput_rate, 2),
                    "days_tracked": oldest_task,
                    "total_completed": len(completed_tasks),
                }

        # Identify bottleneck tasks (long execution times or blocked)
        bottleneck_tasks = []
        for task in tasks:
            if task.state == TaskState.BLOCKED:
                bottleneck_tasks.append({
                    "id": task.id,
                    "title": task.title,
                    "reason": "blocked",
                    "error_message": task.error_message,
                })
            elif task.execution_time and task.execution_time > 0:
                avg_time = metrics["average_execution_time"]
                if avg_time and task.execution_time > avg_time * 2:
                    bottleneck_tasks.append({
                        "id": task.id,
                        "title": task.title,
                        "reason": "slow_execution",
                        "execution_time": task.execution_time,
                        "average_time": avg_time,
                    })

        metrics["bottleneck_tasks"] = bottleneck_tasks[:5]  # Top 5 bottlenecks

        return metrics

    def calculate_health_score(self, tasks: List[TaskInfo]) -> Dict[str, any]:
        """Calculate overall project health score."""
        if not tasks:
            return {"score": 100, "status": "no_tasks", "factors": {}}

        factors = {}
        total_score = 100

        # Factor 1: Progress balance (not too many blocked tasks)
        total_tasks = len(tasks)
        blocked_tasks = sum(1 for task in tasks if task.state == TaskState.BLOCKED)
        blocked_ratio = blocked_tasks / total_tasks if total_tasks > 0 else 0

        if blocked_ratio > 0.3:
            blocked_penalty = 30
        elif blocked_ratio > 0.1:
            blocked_penalty = 10
        else:
            blocked_penalty = 0

        factors["blocked_tasks"] = {
            "ratio": round(blocked_ratio, 2),
            "penalty": blocked_penalty,
            "status": "critical" if blocked_ratio > 0.3 else "warning" if blocked_ratio > 0.1 else "good"
        }
        total_score -= blocked_penalty

        # Factor 2: Progress velocity (steady completion rate)
        completed_tasks = sum(1 for task in tasks if task.state == TaskState.COMPLETED)
        in_progress_tasks = sum(1 for task in tasks if task.state == TaskState.IN_PROGRESS)

        if completed_tasks > 0:
            completion_ratio = completed_tasks / total_tasks
            if in_progress_tasks > completed_tasks * 2:
                # Too many tasks in progress, not completing
                velocity_penalty = 15
                velocity_status = "warning"
            else:
                velocity_penalty = 0
                velocity_status = "good"
        else:
            velocity_penalty = 0
            velocity_status = "no_progress"

        factors["velocity"] = {
            "completed": completed_tasks,
            "in_progress": in_progress_tasks,
            "penalty": velocity_penalty,
            "status": velocity_status
        }
        total_score -= velocity_penalty

        # Factor 3: Task age (how long are tasks pending)
        now = datetime.now()
        old_tasks = 0
        for task in tasks:
            if task.state in [TaskState.PENDING, TaskState.IN_PROGRESS]:
                if task.last_updated:
                    age_days = (now - task.last_updated).days
                    if age_days > 7:  # Tasks older than a week
                        old_tasks += 1

        old_ratio = old_tasks / total_tasks if total_tasks > 0 else 0
        if old_ratio > 0.5:
            age_penalty = 20
        elif old_ratio > 0.2:
            age_penalty = 10
        else:
            age_penalty = 0

        factors["task_age"] = {
            "old_tasks": old_tasks,
            "ratio": round(old_ratio, 2),
            "penalty": age_penalty,
            "status": "critical" if old_ratio > 0.5 else "warning" if old_ratio > 0.2 else "good"
        }
        total_score -= age_penalty

        # Determine overall status
        total_score = max(0, total_score)  # Don't go below 0
        if total_score >= 80:
            status = "excellent"
        elif total_score >= 60:
            status = "good"
        elif total_score >= 40:
            status = "fair"
        else:
            status = "poor"

        return {
            "score": total_score,
            "status": status,
            "factors": factors
        }

    def estimate_completion_time(self, tasks: List[TaskInfo], history: List[TaskHistory]) -> Optional[Dict[str, any]]:
        """Estimate completion time based on current progress and historical data."""
        remaining_tasks = [
            task for task in tasks
            if task.state in [TaskState.PENDING, TaskState.IN_PROGRESS]
        ]

        if not remaining_tasks:
            return {"status": "completed", "estimated_days": 0}

        # Calculate recent completion rate
        recent_history = [
            entry for entry in history
            if entry.new_state == TaskState.COMPLETED
            and (datetime.now() - entry.timestamp).days <= 7
        ]

        if not recent_history:
            return {"status": "no_history", "estimated_days": None}

        completion_rate = len(recent_history) / 7  # tasks per day

        if completion_rate <= 0:
            return {"status": "stalled", "estimated_days": None}

        # Consider task estimates if available
        total_remaining_hours = sum(
            task.estimated_hours or 1.0 for task in remaining_tasks
        )

        # Get average execution time from completed tasks
        completed_with_time = [
            task for task in tasks
            if task.state == TaskState.COMPLETED and task.execution_time
        ]

        if completed_with_time:
            avg_hours_per_task = statistics.mean(task.execution_time for task in completed_with_time)
            estimated_days = max(1, math.ceil(total_remaining_hours / (avg_hours_per_task * completion_rate)))
        else:
            # Simple task count estimate
            estimated_days = max(1, math.ceil(len(remaining_tasks) / completion_rate))

        return {
            "status": "estimated",
            "estimated_days": estimated_days,
            "completion_date": (datetime.now() + timedelta(days=estimated_days)).date().isoformat(),
            "remaining_tasks": len(remaining_tasks),
            "completion_rate": round(completion_rate, 2),
            "confidence": "high" if len(recent_history) >= 5 else "medium" if len(recent_history) >= 2 else "low"
        }