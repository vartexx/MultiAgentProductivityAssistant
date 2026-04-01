from __future__ import annotations

import os


class Settings:
    app_name: str = os.getenv("APP_NAME", "Multi-Agent Productivity Assistant")
    api_prefix: str = os.getenv("API_PREFIX", "/api/v1")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./productivity.db")

    # Optional MCP endpoints. If unset, built-in local mock behavior is used.
    calendar_mcp_url: str | None = os.getenv("CALENDAR_MCP_URL")
    task_mcp_url: str | None = os.getenv("TASK_MCP_URL")
    notes_mcp_url: str | None = os.getenv("NOTES_MCP_URL")


settings = Settings()
