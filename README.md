# Multi-Agent Productivity Assistant

An API-based multi-agent system that coordinates planning, scheduling, and knowledge capture across MCP-compatible tools and persists data in a database.

## What This Demonstrates

- Primary orchestrator agent coordinating specialized sub-agents
- Structured persistence with SQLite via SQLAlchemy
- MCP-style tool integration for calendar, task manager, and notes
- Multi-step workflow execution with execution logs
- FastAPI deployment surface for real-world integrations

## Architecture

- **Primary Agent**: `ProductivityOrchestrator`
- **Sub-Agents**:
  - `PlannerAgent` creates executable steps from user goals
  - `SchedulerAgent` maps each step to a specific MCP tool
  - `KnowledgeAgent` generates workflow summaries
- **MCP Tool Layer**: `MCPToolRegistry` and `MCPToolClient`
- **Data Layer**:
  - `tasks`
  - `notes`
  - `workflow_runs`
  - `tool_executions`

## API Endpoints

- `GET /`
- `GET /health`
- `POST /api/v1/workflows/execute`
- `POST /api/v1/tasks`
- `GET /api/v1/tasks?user_id=<id>`
- `POST /api/v1/notes`
- `GET /api/v1/notes?user_id=<id>`
- `GET /api/v1/workflow-runs?user_id=<id>`

## Quick Start

```bash
cd C:/Users/Harsh/MultiAgentProductivityAssistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open: `http://127.0.0.1:8000/docs`

## Example Workflow Request

```json
{
  "user_id": "user-123",
  "goal": "Schedule my meetings, generate tasks, and capture notes",
  "context": {
    "timeframe": "this week",
    "due_date": "2026-04-02",
    "priority": "high"
  }
}
```

## MCP Integration Notes

Set optional environment variables to connect to external MCP servers:

- `CALENDAR_MCP_URL`
- `TASK_MCP_URL`
- `NOTES_MCP_URL`

If not set, built-in mock execution is used so the system can run locally.
