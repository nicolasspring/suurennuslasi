import typing as t

from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: t.Optional[str] = "success"
    message: t.Optional[str] = None
