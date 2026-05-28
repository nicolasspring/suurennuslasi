import os
from contextlib import asynccontextmanager

import aioboto3
from botocore.config import Config

session = aioboto3.Session()
config = Config(signature_version="s3v4")
minio_bucket_name = os.getenv("MINIO_BUCKET_NAME")


@asynccontextmanager
async def get_minio_client():
    async with session.client(
        "s3",
        endpoint_url=os.getenv("MINIO_ENDPOINT"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        config=config,
    ) as client:
        yield client
