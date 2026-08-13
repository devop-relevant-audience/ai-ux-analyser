from datetime import datetime
from typing import Any

from sqlalchemy import JSON
from sqlmodel import Field, SQLModel

class Run (SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)

  url: str

  timestamp: datetime = Field(default_factory=datetime.now)

  screenshots: dict[str, Any] = Field(sa_type=JSON)

  report: dict[str, Any] = Field(sa_type=JSON)
