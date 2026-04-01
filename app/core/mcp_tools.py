from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

import httpx


@dataclass
class MCPExecutionResult:
    success: bool
    data: dict


class MCPToolClient:
    def __init__(self, tool_name: str, endpoint: str | None = None) -> None:
        self.tool_name = tool_name
        self.endpoint = endpoint

    async def execute(self, action: str, payload: dict) -> MCPExecutionResult:
        if self.endpoint:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(self.endpoint, json={"tool": self.tool_name, "action": action, "payload": payload})
                response.raise_for_status()
                return MCPExecutionResult(success=True, data=response.json())

        # Local mock path for demo environments without MCP servers.
        now = datetime.now(UTC).isoformat()
        return MCPExecutionResult(
            success=True,
            data={
                "tool": self.tool_name,
                "action": action,
                "payload": payload,
                "executed_at": now,
                "message": f"{self.tool_name} handled '{action}'",
            },
        )


class MCPToolRegistry:
    def __init__(self, calendar_url: str | None, task_url: str | None, notes_url: str | None) -> None:
        self._tools = {
            "calendar": MCPToolClient("calendar", calendar_url),
            "task_manager": MCPToolClient("task_manager", task_url),
            "notes": MCPToolClient("notes", notes_url),
        }

    def get(self, tool_name: str) -> MCPToolClient:
        if tool_name not in self._tools:
            raise KeyError(f"Unknown tool: {tool_name}")
        return self._tools[tool_name]
