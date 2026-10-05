from functools import lru_cache

from geoparser.db import db as geoparser_db
from geoparser.db.models import (
    Context,
    Document,
    Project,
    Recognition,
    Recognizer,
    Reference,
    Referent,
    Resolution,
    Resolver,
)
from geoparser.project import project as geoparser_project
from sqlalchemy import MetaData

_GEOPARSER_MODELS = (
    Context,
    Document,
    Project,
    Recognition,
    Recognizer,
    Reference,
    Referent,
    Resolution,
    Resolver,
)


@lru_cache(maxsize=1)
def configure_geoparser_database() -> None:
    """Restrict Geoparser schema creation to Geoparser's own models."""
    metadata = MetaData()
    for model in _GEOPARSER_MODELS:
        model.__table__.to_metadata(metadata)

    def create_geoparser_tables() -> None:
        geoparser_db._check_database_compatibility()
        metadata.create_all(geoparser_db.engine)

    # SQLModel.metadata is process-global, so it also contains the service's models.
    geoparser_db.create_db_and_tables = create_geoparser_tables
    geoparser_project.create_db_and_tables = create_geoparser_tables
