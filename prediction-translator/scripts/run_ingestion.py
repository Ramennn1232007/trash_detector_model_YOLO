from app.db import SessionLocal
from app.services.ingest.market_ingestor import run_ingestion


if __name__ == "__main__":
    with SessionLocal() as db:
        inserted = run_ingestion(db)
        print(f"Inserted {inserted} market snapshots")
