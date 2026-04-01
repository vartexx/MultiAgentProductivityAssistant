from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.schemas import (
    NoteCreateRequest,
    NoteResponse,
    TaskCreateRequest,
    TaskResponse,
    WorkflowExecuteRequest,
    WorkflowExecuteResponse,
    WorkflowRunResponse,
)
from app.services.orchestrator import ProductivityOrchestrator

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/workflows/execute", response_model=WorkflowExecuteResponse)
async def execute_workflow(payload: WorkflowExecuteRequest, db: Session = Depends(get_db)) -> dict:
    orchestrator = ProductivityOrchestrator(db)
    return await orchestrator.execute_workflow(user_id=payload.user_id, goal=payload.goal, context=payload.context)


@router.post("/tasks", response_model=TaskResponse)
def create_task(payload: TaskCreateRequest, db: Session = Depends(get_db)) -> dict:
    orchestrator = ProductivityOrchestrator(db)
    return orchestrator.create_task(
        user_id=payload.user_id,
        title=payload.title,
        due_date=payload.due_date,
        metadata=payload.metadata,
    )


@router.get("/tasks", response_model=list[TaskResponse])
def list_tasks(user_id: str | None = None, db: Session = Depends(get_db)) -> list[dict]:
    orchestrator = ProductivityOrchestrator(db)
    return orchestrator.list_tasks(user_id=user_id)


@router.post("/notes", response_model=NoteResponse)
def create_note(payload: NoteCreateRequest, db: Session = Depends(get_db)) -> dict:
    orchestrator = ProductivityOrchestrator(db)
    return orchestrator.create_note(user_id=payload.user_id, title=payload.title, body=payload.body, metadata=payload.metadata)


@router.get("/notes", response_model=list[NoteResponse])
def list_notes(user_id: str | None = None, db: Session = Depends(get_db)) -> list[dict]:
    orchestrator = ProductivityOrchestrator(db)
    return orchestrator.list_notes(user_id=user_id)


@router.get("/workflow-runs", response_model=list[WorkflowRunResponse])
def list_workflow_runs(user_id: str | None = None, db: Session = Depends(get_db)) -> list[dict]:
    orchestrator = ProductivityOrchestrator(db)
    return orchestrator.list_workflow_runs(user_id=user_id)
