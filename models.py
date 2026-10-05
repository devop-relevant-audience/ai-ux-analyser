from datetime import datetime
from typing import Any

from sqlalchemy import JSON
from sqlmodel import Field, SQLModel


class Run(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    page_title: str | None = None
    page_name: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = Field(default="queued")
    screenshots: dict[str, Any] = Field(
        default_factory=dict,
        sa_type=JSON,
    )

    report: dict[str, Any] = Field(
        default_factory=dict,
        sa_type=JSON,
    )
