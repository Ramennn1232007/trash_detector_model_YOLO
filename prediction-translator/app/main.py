from fastapi import FastAPI

from app.api.routes_baskets import router as baskets_router
from app.api.routes_events import router as events_router
from app.api.routes_health import router as health_router
from app.api.routes_signals import router as signals_router
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Prediction Translator MVP")
app.include_router(health_router)
app.include_router(events_router)
app.include_router(signals_router)
app.include_router(baskets_router)


@app.get("/")
def root() -> dict:
    return {"message": "Prediction translator MVP online"}
