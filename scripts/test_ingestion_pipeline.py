from __future__ import annotations

import asyncio
from pathlib import Path

from fastapi import UploadFile

from backend.infrastructure.ingestion import IngestionService


async def main() -> None:
    sample_file = Path("tests/data/sample.pdf")

    if not sample_file.exists():
        raise FileNotFoundError(
            f"Sample file not found: {sample_file.resolve()}"
        )

    print("=" * 60)
    print("Starting ingestion pipeline test...")
    print("=" * 60)

    with sample_file.open("rb") as file:
        upload_file = UploadFile(
            filename=sample_file.name,
            file=file,
        )

        ingestion_service = IngestionService()

        result = await ingestion_service.ingest(upload_file)

    print()
    print("=" * 60)
    print("INGESTION COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print(f"Filename         : {result.filename}")
    print(f"Chunks Created   : {result.chunks_created}")
    print(f"Vectors Uploaded : {result.vectors_uploaded}")

    print()
    print("The document should now be indexed in Qdrant.")


if __name__ == "__main__":
    asyncio.run(main())