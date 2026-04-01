from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlanStep:
    description: str
    action: str
    payload: dict


class PlannerAgent:
    """Primary planning sub-agent that converts goals into executable steps."""

    def plan(self, goal: str, context: dict) -> list[PlanStep]:
        steps: list[PlanStep] = []

        # Build a simple actionable plan from free-form user intent.
        lowered = goal.lower()
        if "schedule" in lowered or "calendar" in lowered or "meeting" in lowered:
            steps.append(
                PlanStep(
                    description="Create or sync calendar events",
                    action="calendar.sync_events",
                    payload={"intent": goal, "timeframe": context.get("timeframe", "this week")},
                )
            )

        steps.append(
            PlanStep(
                description="Create task backlog from goal",
                action="task.create_from_goal",
                payload={"goal": goal, "priority": context.get("priority", "normal")},
            )
        )

        if "note" in lowered or "research" in lowered or "summary" in lowered:
            steps.append(
                PlanStep(
                    description="Capture structured notes",
                    action="notes.capture",
                    payload={"title": "Workflow Notes", "content": goal},
                )
            )

        return steps


class SchedulerAgent:
    """Routing sub-agent that maps actions to concrete MCP tools."""

    def route_tool(self, action: str) -> str:
        if action.startswith("calendar."):
            return "calendar"
        if action.startswith("task."):
            return "task_manager"
        if action.startswith("notes."):
            return "notes"
        return "task_manager"


class KnowledgeAgent:
    """Knowledge sub-agent that builds final execution summaries."""

    def summarize(self, goal: str, step_results: list[dict]) -> str:
        success_count = len([x for x in step_results if x.get("status") == "success"])
        total = len(step_results)
        return f"Goal '{goal}' executed with {success_count}/{total} successful steps."
