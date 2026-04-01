# Demo Script - Multi-Agent Productivity Assistant (3 minutes)

## Opening (15 seconds)
**What to show**: Project title slide or README on screen

"This is the Multi-Agent Productivity Assistant—an AI-powered backend API that takes a user goal and orchestrates multiple agents to plan, schedule, and capture information across MCP-compatible tools. It demonstrates multi-agent coordination, structured data persistence, and workflow automation."

---

## Part 1: Project Architecture (30 seconds)
**What to show**: Open the README.md or draw/show diagram

"The system has three layers:
1. **Agent Layer**: A primary orchestrator with three sub-agents:
   - Planner (breaks goal into steps)
   - Scheduler (routes steps to tools)
   - Knowledge (summarizes results)
   
2. **Tool Layer**: MCP registry for calendar, task manager, and notes tools

3. **Data Layer**: SQLite database with persistence for workflows, tasks, notes, and execution logs"

---

## Part 2: Live API Demo (90 seconds)
**What to show on screen**: Terminal or browser

### 2.1 Start the server (10 seconds)
```bash
cd C:\Users\Harsh\MultiAgentProductivityAssistant
.venv\Scripts\activate
uvicorn app.main:app --reload
```
**Say**: "The API starts instantly. It initializes SQLite and exposes Swagger documentation at /docs."

### 2.2 Show Swagger UI (20 seconds)
**What to show**: Open http://127.0.0.1:8000/docs in browser
**Say**: "Here's the interactive API documentation. Users can see all endpoints:
- Execute workflow
- Create/list tasks
- Create/list notes
- View workflow runs"

### 2.3 Execute a workflow (60 seconds)
**What to show**: In Swagger, click on `/api/v1/workflows/execute` → Try it out

**Request body**:
```json
{
  "user_id": "demo-user-123",
  "goal": "Schedule a team standup meeting, create follow-up tasks, and capture meeting notes",
  "context": {
    "timeframe": "this week",
    "due_date": "2026-04-02",
    "priority": "high"
  }
}
```

**Say**: "I'm sending a goal to the system. The orchestrator will:
1. Plan three steps: calendar sync, task creation, and note capture
2. Route each to the appropriate MCP tool
3. Execute and log each step
4. Return a summary and step results"

**Execute** and show response. Point out:
- workflow_run_id (unique identifier)
- status (success)
- steps array showing planner/tool/action/result for each step
- summary with count of successful steps

### 2.4 Verify persistence (20 seconds)
**What to show**: Call other endpoints

**Execute**: GET `/api/v1/tasks?user_id=demo-user-123`
**Say**: "The task created automatically by the workflow is now persisted and queryable."

**Execute**: GET `/api/v1/workflow-runs?user_id=demo-user-123`
**Say**: "And the workflow run is logged for audit and history."

---

## Part 3: Key Features (15 seconds)
**What to show**: Highlight in code comments or terminal output

1. **Multi-Agent Coordination**: Primary agent coordinates 3 sub-agents
2. **Tool Integration**: MCP registry supports pluggable external services
3. **Persistence**: SQLite + SQLAlchemy for structured data
4. **Validation**: Pydantic schemas enforce data types (e.g., dates)
5. **Testing**: 7 passing integration tests
6. **UTC Timestamps**: ISO-8601 formatted timestamps with Z suffix for consistency

---

## Closing (15 seconds)
**What to show**: GitHub repo link on screen

"This is a hackathon-ready prototype that demonstrates:
- Multi-agent orchestration for complex workflows
- Integration with external tools via MCP
- Persistent data storage and retrieval
- Production-ready API with automatic docs

The code is open source on GitHub: https://github.com/vartexx/MultiAgentProductivityAssistant

All links are public and live. The API is deployed on Cloud Run and running at [SERVICE_URL]."

---

## Quick Reference: PowerShell Commands for Demo

```powershell
# Start API
cd C:\Users\Harsh\MultiAgentProductivityAssistant
.venv\Scripts\activate
uvicorn app.main:app --reload

# In another terminal, test endpoints
$BASE_URL = "http://localhost:8000"

# Health check
curl "$BASE_URL/health"

# Execute workflow (PowerShell)
$body = @{
    user_id = "demo-user-123"
    goal = "Schedule a team standup meeting, create follow-up tasks, and capture meeting notes"
    context = @{
        timeframe = "this week"
        due_date = "2026-04-02"
        priority = "high"
    }
} | ConvertTo-Json

curl -Method POST "$BASE_URL/api/v1/workflows/execute" -Body $body -ContentType "application/json"

# List tasks
curl "$BASE_URL/api/v1/tasks?user_id=demo-user-123"

# List workflow runs
curl "$BASE_URL/api/v1/workflow-runs?user_id=demo-user-123"
```

---

## Pro Tips for Demo

1. **Network**: Have terminal and browser side-by-side
2. **Timing**: Actually pause between sections—the demo is fast!
3. **Fail gracefully**: If something breaks, show the test output (`pytest -q`) to prove it works
4. **Engagement**: Ask the audience: "How would you extend this with your own agents?"
