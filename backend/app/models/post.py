from datetime import datetime

from sqlmodel import SQLModel, Field


class Post(SQLModel, table=True):
    id: str = Field(primary_key=True)
    caption: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    created_at: datetime | None = None
