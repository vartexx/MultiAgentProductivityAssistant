from app.core.agents import PlannerAgent, SchedulerAgent


def test_planner_generates_task_step() -> None:
    planner = PlannerAgent()
    steps = planner.plan("Plan my week", {"priority": "high"})
    actions = [step.action for step in steps]
    assert "task.create_from_goal" in actions


def test_scheduler_routes_tools() -> None:
    scheduler = SchedulerAgent()
    assert scheduler.route_tool("calendar.sync_events") == "calendar"
    assert scheduler.route_tool("task.create_from_goal") == "task_manager"
    assert scheduler.route_tool("notes.capture") == "notes"
