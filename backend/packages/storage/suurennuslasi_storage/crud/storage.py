import typing as t

import aiofiles
from botocore.exceptions import ClientError

from suurennuslasi_storage.session import (
    get_object_storage_client,
    object_storage_bucket_name,
)


class AsyncObjectStorage:
    @staticmethod
    async def bucket_exists(bucket: str | None = None) -> bool:
        bucket = bucket or object_storage_bucket_name
        async with get_object_storage_client() as object_storage_client:
            try:
                await object_storage_client.head_bucket(Bucket=bucket)
                return True
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in {"404", "NoSuchBucket"}:
                    return False
                raise

    @staticmethod
    async def create_bucket(bucket: str | None = None):
        bucket = bucket or object_storage_bucket_name
        async with get_object_storage_client() as object_storage_client:
            try:
                await object_storage_client.create_bucket(Bucket=bucket)
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in {"BucketAlreadyOwnedByYou", "BucketAlreadyExists"}:
                    return
                raise

    @staticmethod
    async def upload(key: str, fileobj: t.IO):
        async with get_object_storage_client() as object_storage_client:
            await object_storage_client.upload_fileobj(
                fileobj, object_storage_bucket_name, key
            )

    @staticmethod
    async def download_to_path(key: str, path: str):
        async with get_object_storage_client() as object_storage_client:
            async with aiofiles.open(path, "wb") as file:
                await object_storage_client.download_fileobj(
                    object_storage_bucket_name, key, Fileobj=file
                )

    @staticmethod
    async def delete(key: str):
        async with get_object_storage_client() as object_storage_client:
            await object_storage_client.delete_object(
                Bucket=object_storage_bucket_name, Key=key
            )
