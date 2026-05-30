from uuid import UUID

from pydantic import BaseModel


class ImportCreated(BaseModel):
    job_id: UUID
    object_key: str
