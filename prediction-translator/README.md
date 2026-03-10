# Prediction Translator MVP (Scaffold)

This folder adds a focused MVP scaffold for translating prediction-market probability changes into stock-basket signals.

## Included in this scaffold

- FastAPI backend skeleton
- SQLAlchemy models for the MVP schema (`venues`, `events`, `markets`, snapshots, baskets, links, signals)
- Rule-based event normalizer for three initial families: rates, energy, recession
- Seed exposure registry for initial event→basket links
- Signal scoring utilities (expected move, lag gap, weighted final score, explanation builder)
- Minimal API routes:
  - `GET /health`
  - `GET /events/movers`
  - `GET /signals`
  - `GET /baskets`
- Script entrypoints:
  - `scripts/run_ingestion.py`
  - `scripts/run_scoring.py`

## Run locally

```bash
cd prediction-translator
PYTHONPATH=. uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs`.

## Notes

- Venue clients are intentionally stubbed now with consistent normalized payloads to validate flow.
- Replace the clients with Kalshi/Polymarket real API integrations next.
