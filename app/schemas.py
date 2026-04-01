from __future__ import annotations

from datetime import UTC, date, datetime

from pydantic import BaseModel, Field, field_serializer


class WorkflowExecuteRequest(BaseModel):
    user_id: str = Field(..., examples=["user-123"])
    goal: str = Field(..., examples=["Plan my week and capture meeting notes"])
    context: dict = Field(default_factory=dict)


class WorkflowStepResult(BaseModel):
    step: str
    tool: str
    action: str
    status: str
    result: dict


class WorkflowExecuteResponse(BaseModel):
    workflow_run_id: int
    status: str
    summary: str
    steps: list[WorkflowStepResult]


class TaskCreateRequest(BaseModel):
    user_id: str
    title: str
    due_date: date | None = None
    metadata: dict = Field(default_factory=dict)


class CreatedAtUTCModel(BaseModel):
    @field_serializer("created_at", check_fields=False)
    def serialize_created_at(self, value: datetime) -> str:
        utc_value = value if value.tzinfo is not None else value.replace(tzinfo=UTC)
        return utc_value.astimezone(UTC).isoformat().replace("+00:00", "Z")


class TaskResponse(CreatedAtUTCModel):
    id: int
    user_id: str
    title: str
    status: str
    due_date: date | None
    metadata: dict
    created_at: datetime


class NoteCreateRequest(BaseModel):
    user_id: str
    title: str
    body: str
    metadata: dict = Field(default_factory=dict)


class NoteResponse(CreatedAtUTCModel):
    id: int
    user_id: str
    title: str
    body: str
    metadata: dict
    created_at: datetime


class WorkflowRunResponse(CreatedAtUTCModel):
    id: int
    user_id: str
    goal: str
    status: str
    summary: str
    created_at: datetime
