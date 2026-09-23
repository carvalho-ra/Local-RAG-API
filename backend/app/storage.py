from minio import Minio
import os


client = Minio(
    os.environ["MINIO_ENDPOINT"],
    access_key=os.environ["MINIO_ACCESS_KEY"],
    secret_key=os.environ["MINIO_SECRET_KEY"],
    secure=False,
)

MINIO_BUCKET = os.environ["MINIO_BUCKET"]

def upload_file(file_data, storage_key, content_type):
    client.put_object(
        MINIO_BUCKET,
        storage_key,
        file_data,
        length=-1,
        part_size=10 * 1024 * 1024,
        content_type=content_type,
    )

    return storage_key

def download_file(storage_key):
    response = client.get_object(
        MINIO_BUCKET,
        storage_key,
    )

    try:
        return response.read()
    finally:
        response.close()
        response.release_conn()
