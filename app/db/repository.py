from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import NoteRecord, TaskRecord, ToolExecution, WorkflowRun


class Repository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_task(self, user_id: str, title: str, due_date: str | None = None, metadata: dict | None = None) -> TaskRecord:
        task = TaskRecord(
            user_id=user_id,
            title=title,
            status="pending",
            due_date=due_date,
            metadata_json=metadata or {},
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def list_tasks(self, user_id: str | None = None) -> list[TaskRecord]:
        query = self.db.query(TaskRecord)
        if user_id:
            query = query.filter(TaskRecord.user_id == user_id)
        return query.order_by(TaskRecord.created_at.desc()).all()

    def create_note(self, user_id: str, title: str, body: str, metadata: dict | None = None) -> NoteRecord:
        note = NoteRecord(user_id=user_id, title=title, body=body, metadata_json=metadata or {})
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def list_notes(self, user_id: str | None = None) -> list[NoteRecord]:
        query = self.db.query(NoteRecord)
        if user_id:
            query = query.filter(NoteRecord.user_id == user_id)
        return query.order_by(NoteRecord.created_at.desc()).all()

    def create_workflow_run(self, user_id: str, goal: str) -> WorkflowRun:
        run = WorkflowRun(user_id=user_id, goal=goal, status="running", summary="")
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def finish_workflow_run(self, run_id: int, status: str, summary: str) -> WorkflowRun:
        run = self.db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
        if run is None:
            raise ValueError(f"Workflow run {run_id} not found")
        run.status = status
        run.summary = summary
        self.db.commit()
        self.db.refresh(run)
        return run

    def list_workflow_runs(self, user_id: str | None = None) -> list[WorkflowRun]:
        query = self.db.query(WorkflowRun)
        if user_id:
            query = query.filter(WorkflowRun.user_id == user_id)
        return query.order_by(WorkflowRun.created_at.desc()).all()

    def log_tool_execution(
        self,
        workflow_run_id: int,
        tool_name: str,
        action: str,
        payload: dict,
        result: dict,
        status: str,
    ) -> ToolExecution:
        execution = ToolExecution(
            workflow_run_id=workflow_run_id,
            tool_name=tool_name,
            action=action,
            payload=payload,
            result=result,
            status=status,
        )
        self.db.add(execution)
        self.db.commit()
        self.db.refresh(execution)
        return execution
