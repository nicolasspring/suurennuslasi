import re
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


class SOURCE_TYPE(str, Enum):
    ZIP = "zip"


POST_HEADER_LOCATION_SPLIT_PATTERN = re.compile(r"\s[\-\u2013\u2014]\s")
