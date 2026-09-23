from app.storage import upload_file, client, download_file
import os
from io import BytesIO
from uuid import uuid4

MINIO_BUCKET = os.environ["MINIO_BUCKET"]


def test_upload_file():
    with open("tests/fixtures/test.pdf", "rb") as file:
        result = upload_file(
            file,
            "test.pdf",
            "application/pdf",
        )

    assert result == "test.pdf"
    assert client.stat_object(MINIO_BUCKET, result)


def test_download_file():
    with open("tests/fixtures/test.pdf", "rb") as file:
        original = file.read()
    
    storage_key = f"test-{uuid4()}.txt"

    upload_file(
        BytesIO(original),
        storage_key,
        "text/plain",
    )

    downloaded = download_file(storage_key)

    assert downloaded == original