from app.storage import upload_file, client
import os

MINIO_BUCKET = os.environ["MINIO_BUCKET"]

def test_upload_file():
    file = open("tests/fixtures/test.pdf", "rb")

    result = upload_file(
        file,
        "test.pdf",
        "application/pdf",
        )

    assert result == 'test.pdf'
    assert client.stat_object(MINIO_BUCKET, result)
