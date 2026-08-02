from .job import ImportJob, ImportJobCreate, ImportJobRead, ImportJobUpdate
from .media import Media, MediaCreate, MediaRead, MediaUpdate
from .post import Post, PostCreate, PostRead, PostUpdate
from .source import Source, SourceCreate, SourceRead, SourceUpdate

for model in (
    ImportJob,
    ImportJobCreate,
    ImportJobRead,
    ImportJobUpdate,
    Media,
    MediaCreate,
    MediaRead,
    MediaUpdate,
    Post,
    PostCreate,
    PostRead,
    PostUpdate,
    Source,
    SourceCreate,
    SourceRead,
    SourceUpdate,
):
    model.model_rebuild()
