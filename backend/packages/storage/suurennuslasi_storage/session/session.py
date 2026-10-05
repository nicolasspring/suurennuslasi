import os
from contextlib import asynccontextmanager

import aioboto3
from botocore.config import Config

session = aioboto3.Session()
config = Config(signature_version="s3v4")
object_storage_bucket_name = os.getenv("OBJECT_STORAGE_BUCKET_NAME")


@asynccontextmanager
async def get_object_storage_client():
    async with session.client(
        "s3",
        endpoint_url=f"http://{os.getenv("OBJECT_STORAGE_ENDPOINT")}",
        aws_access_key_id=os.getenv("OBJECT_STORAGE_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("OBJECT_STORAGE_SECRET_KEY"),
        config=config,
    ) as client:
        yield client
