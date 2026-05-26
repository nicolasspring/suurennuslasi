from enum import Enum


class IMPORT_JOB_STATUS(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    EXTRACTING = "extracting"
    PARSING = "parsing"
    GEOPARSING = "geoparsing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
