from dotenv import load_dotenv

load_dotenv()

import asyncio

from app.database import SessionLocal
from app.services.ingestion import ingest_document


async def main():
    db = SessionLocal()

    try:
        with open("tests/fixtures/test.pdf", "rb") as file:
            await ingest_document(
                db,
                file,
                "test.pdf",
                "application/pdf",
            )
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())