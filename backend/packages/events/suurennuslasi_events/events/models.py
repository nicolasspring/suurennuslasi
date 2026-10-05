from uuid import UUID

from pydantic import BaseModel


class ImportCreated(BaseModel):
    job_id: UUID
    object_key: str
    source_id: UUID


class PostExtracted(BaseModel):
    job_id: UUID
    post_id: UUID


class PostParsed(BaseModel):
    job_id: UUID
    post_id: UUID
