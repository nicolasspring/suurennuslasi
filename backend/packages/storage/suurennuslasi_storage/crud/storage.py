import typing as t

import aiofiles
from botocore.exceptions import ClientError

from suurennuslasi_storage.session import get_minio_client, minio_bucket_name


class AsyncObjectStorage:
    @staticmethod
    async def create_bucket():
        async with get_minio_client() as minio_client:
            try:
                await minio_client.create_bucket(bucket=minio_bucket_name)
            except ClientError as e:
                pass  # bucket exists already

    @staticmethod
    async def upload(key: str, fileobj: t.IO):
        async with get_minio_client() as minio_client:
            await minio_client.upload_fileobj(fileobj, minio_bucket_name, key)

    @staticmethod
    async def download_to_path(key: str, path: str):
        async with get_minio_client() as minio_client:
            async with aiofiles.open(path, "wb") as file:
                minio_client.download_fileobj(minio_bucket_name, key, file)

    @staticmethod
    async def delete(key: str):
        async with get_minio_client() as minio_client:
            minio_client.delete_object(minio_bucket_name, key)
