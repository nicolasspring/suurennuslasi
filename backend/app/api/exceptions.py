from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.models.api import BaseResponse


class ImportJobNotFoundException(Exception):
    pass


class PostNotFoundException(Exception):
    pass


def import_job_exception_handler(
    request: Request, exc: ImportJobNotFoundException
) -> JSONResponse:
    return JSONResponse(
        content={**BaseResponse(status="error", message="Job not found.").model_dump()},
        status_code=status.HTTP_404_NOT_FOUND,
    )


def post_exception_handler(
    request: Request, exc: PostNotFoundException
) -> JSONResponse:
    return JSONResponse(
        content={
            **BaseResponse(status="error", message="Post not found.").model_dump()
        },
        status_code=status.HTTP_404_NOT_FOUND,
    )
