from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.config import settings
from app.core.agents import KnowledgeAgent, PlannerAgent, SchedulerAgent
from app.core.mcp_tools import MCPToolRegistry
from app.db.repository import Repository


class ProductivityOrchestrator:
    def __init__(self, db: Session) -> None:
        self.repo = Repository(db)
        self.planner = PlannerAgent()
        self.scheduler = SchedulerAgent()
        self.knowledge = KnowledgeAgent()
        self.tools = MCPToolRegistry(
            calendar_url=settings.calendar_mcp_url,
            task_url=settings.task_mcp_url,
            notes_url=settings.notes_mcp_url,
        )

    async def execute_workflow(self, user_id: str, goal: str, context: dict) -> dict:
        workflow_run = self.repo.create_workflow_run(user_id=user_id, goal=goal)
        plan = self.planner.plan(goal=goal, context=context)

        step_results: list[dict] = []
        workflow_status = "success"

        for step in plan:
            tool_name = self.scheduler.route_tool(step.action)
            tool = self.tools.get(tool_name)
            payload = {"user_id": user_id, **step.payload}

            try:
                tool_result = await tool.execute(action=step.action, payload=payload)
                status = "success" if tool_result.success else "failed"
            except Exception as ex:  # noqa: BLE001
                status = "failed"
                tool_result = type("FailedResult", (), {"data": {"error": str(ex)}, "success": False})

            if status == "success" and step.action == "task.create_from_goal":
                workflow_due_date = context.get("due_date")
                if isinstance(workflow_due_date, date):
                    workflow_due_date = workflow_due_date.isoformat()
                task = self.repo.create_task(
                    user_id=user_id,
                    title=f"Action for: {goal}",
                    due_date=workflow_due_date,
                    metadata={"source": "workflow", "tool_result": tool_result.data},
                )
                tool_result.data["task_id"] = task.id

            if status == "success" and step.action == "notes.capture":
                note = self.repo.create_note(
                    user_id=user_id,
                    title=step.payload.get("title", "Workflow Note"),
                    body=step.payload.get("content", goal),
                    metadata={"source": "workflow", "tool_result": tool_result.data},
                )
                tool_result.data["note_id"] = note.id

            if status == "failed":
                workflow_status = "failed"

            self.repo.log_tool_execution(
                workflow_run_id=workflow_run.id,
                tool_name=tool_name,
                action=step.action,
                payload=payload,
                result=tool_result.data,
                status=status,
            )

            step_results.append(
                {
                    "step": step.description,
                    "tool": tool_name,
                    "action": step.action,
                    "status": status,
                    "result": tool_result.data,
                }
            )

        summary = self.knowledge.summarize(goal, step_results)
        self.repo.finish_workflow_run(workflow_run.id, status=workflow_status, summary=summary)

        return {
            "workflow_run_id": workflow_run.id,
            "status": workflow_status,
            "summary": summary,
            "steps": step_results,
        }

    def create_task(self, user_id: str, title: str, due_date: date | None, metadata: dict) -> dict:
        normalized_due_date = due_date.isoformat() if due_date else None
        task = self.repo.create_task(user_id=user_id, title=title, due_date=normalized_due_date, metadata=metadata)
        return {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "status": task.status,
            "due_date": task.due_date,
            "metadata": task.metadata_json,
            "created_at": task.created_at,
        }

    def list_notes(self, user_id: str | None = None) -> list[dict]:
        rows = self.repo.list_notes(user_id=user_id)
        return [
            {
                "id": row.id,
                "user_id": row.user_id,
                "title": row.title,
                "body": row.body,
                "metadata": row.metadata_json,
                "created_at": row.created_at,
            }
            for row in rows
        ]

    def list_tasks(self, user_id: str | None = None) -> list[dict]:
        rows = self.repo.list_tasks(user_id=user_id)
        return [
            {
                "id": row.id,
                "user_id": row.user_id,
                "title": row.title,
                "status": row.status,
                "due_date": row.due_date,
                "metadata": row.metadata_json,
                "created_at": row.created_at,
            }
            for row in rows
        ]

    def create_note(self, user_id: str, title: str, body: str, metadata: dict) -> dict:
        note = self.repo.create_note(user_id=user_id, title=title, body=body, metadata=metadata)
        return {
            "id": note.id,
            "user_id": note.user_id,
            "title": note.title,
            "body": note.body,
            "metadata": note.metadata_json,
            "created_at": note.created_at,
        }

    def list_workflow_runs(self, user_id: str | None = None) -> list[dict]:
        rows = self.repo.list_workflow_runs(user_id=user_id)
        return [
            {
                "id": row.id,
                "user_id": row.user_id,
                "goal": row.goal,
                "status": row.status,
                "summary": row.summary,
                "created_at": row.created_at,
            }
            for row in rows
        ]
