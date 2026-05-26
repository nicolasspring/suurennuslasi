from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from suurennuslasi_api.exceptions import (
    import_job_exception_handler,
    post_exception_handler,
)
from suurennuslasi_api.routes.ingestion import router as ingestion_router
from suurennuslasi_api.routes.posts import router as posts_router

from suurennuslasi_db.crud.exceptions import (
    ImportJobNotFoundException,
    PostNotFoundException,
)
from suurennuslasi_db.session.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(ImportJobNotFoundException, import_job_exception_handler)
app.add_exception_handler(PostNotFoundException, post_exception_handler)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion_router)
app.include_router(posts_router)
