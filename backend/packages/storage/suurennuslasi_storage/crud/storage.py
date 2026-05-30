import typing as t

import aiofiles
from botocore.exceptions import ClientError

from suurennuslasi_storage.session import get_minio_client, minio_bucket_name


class AsyncObjectStorage:
    @staticmethod
    async def bucket_exists(bucket: str | None = None) -> bool:
        bucket = bucket or minio_bucket_name
        async with get_minio_client() as minio_client:
            try:
                await minio_client.head_bucket(Bucket=bucket)
                return True
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in {"404", "NoSuchBucket"}:
                    return False
                raise

    @staticmethod
    async def create_bucket(bucket: str | None = None):
        bucket = bucket or minio_bucket_name
        async with get_minio_client() as minio_client:
            try:
                await minio_client.create_bucket(Bucket=bucket)
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code in {"BucketAlreadyOwnedByYou", "BucketAlreadyExists"}:
                    return
                raise

    @staticmethod
    async def upload(key: str, fileobj: t.IO):
        async with get_minio_client() as minio_client:
            await minio_client.upload_fileobj(fileobj, minio_bucket_name, key)

    @staticmethod
    async def download_to_path(key: str, path: str):
        async with get_minio_client() as minio_client:
            async with aiofiles.open(path, "wb") as file:
                await minio_client.download_fileobj(
                    minio_bucket_name, key, Fileobj=file
                )

    @staticmethod
    async def delete(key: str):
        async with get_minio_client() as minio_client:
            await minio_client.delete_object(Bucket=minio_bucket_name, Key=key)
