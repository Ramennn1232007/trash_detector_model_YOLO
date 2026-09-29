"""Live trash counter: camera -> YOLOv10 -> DeepSORT -> count, with a small FastAPI server.

Run:  python main.py
Settings come from environment variables (see .env.example).
"""
import asyncio
import datetime
import json
import logging
import os
import threading
import time

import cv2
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pipeline import CounterState, TrashCounter
from utils.alert_system import send_alert
from utils.camera import initialize_camera

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "models/best_one_class.pt")
CONF_THRESHOLD = float(os.getenv("CONF_THRESHOLD", "0.25"))
TRASH_THRESHOLD = int(os.getenv("TRASH_THRESHOLD", "5"))
CAMERA_SOURCE = os.getenv("CAMERA_SOURCE", "0")
SHOW_WINDOW = os.getenv("SHOW_WINDOW", "false").lower() == "true"
EVENTS_FILE = os.getenv("EVENTS_FILE", "detections.jsonl")
S3_BUCKET = os.getenv("S3_BUCKET")
API_KEY = os.getenv("API_KEY")  # if set, POST endpoints require an X-API-Key header
MAX_FAILED_READS = 50

logging.basicConfig(
    filename="detection_log.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

state = CounterState()
app = FastAPI(title="Trash Detection API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def _check_key(x_api_key):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid API key")


class PHReading(BaseModel):
    pH: float
    sensor_id: str


@app.post("/log-ph")
def log_ph(reading: PHReading, x_api_key: str | None = Header(default=None)):
    """For a real pH sensor only. Nothing in this repo generates pH values."""
    _check_key(x_api_key)
    if not 0 <= reading.pH <= 14:
        raise HTTPException(status_code=422, detail="pH must be between 0 and 14")
    logging.info("sensor_ph sensor_id=%s value=%.2f", reading.sensor_id, reading.pH)
    return {"status": "success"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/status")
def status():
    return {"status": "Monitoring", "model": os.path.basename(MODEL_PATH), "conf_threshold": CONF_THRESHOLD}


@app.get("/trash-count")
def trash_count():
    snap = state.snapshot()
    return {"count": snap["total"], **snap}


@app.websocket("/ws/trash-count")
async def ws_trash_count(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            snap = state.snapshot()
            await websocket.send_json({"count": snap["total"], **snap})
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass


def _upload_events():
    if not S3_BUCKET:
        return
    from aws_integration import upload_to_s3
    key = f"events/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_detections.jsonl"
    ok = upload_to_s3(EVENTS_FILE, S3_BUCKET, key)
    logging.info("s3_upload key=%s ok=%s", key, ok)


def detection_loop():
    counter = TrashCounter(MODEL_PATH, CONF_THRESHOLD)
    cap = initialize_camera(CAMERA_SOURCE)
    failed_reads = 0

    with open(EVENTS_FILE, "a") as events_out:
        while True:
            ok, frame = cap.read()
            if not ok:
                if not CAMERA_SOURCE.isdigit():  # a video file simply ended
                    logging.info("video_ended source=%s total=%d", CAMERA_SOURCE, state.snapshot()["total"])
                    break
                failed_reads += 1
                if failed_reads >= MAX_FAILED_READS:
                    logging.error("camera_lost failed_reads=%d, stopping", failed_reads)
                    break
                time.sleep(0.1)
                continue
            failed_reads = 0

            tracks, events = counter.process(frame)
            for ev in events:
                record = {"timestamp": datetime.datetime.now().isoformat(timespec="seconds"), **ev.__dict__}
                events_out.write(json.dumps(record) + "\n")
                logging.info("counted track_id=%s class=%s conf=%.3f", ev.track_id, ev.class_name, ev.confidence)
            if events:
                events_out.flush()
                state.add(len(events))

            snap = state.snapshot()
            if snap["since_last_alert"] >= TRASH_THRESHOLD:
                send_alert(f"Trash alert: {snap['since_last_alert']} new item(s) detected ({snap['total']} total).")
                logging.info("alert_queued since_last_alert=%d threshold=%d", snap["since_last_alert"], TRASH_THRESHOLD)
                state.reset_alert_window()
                threading.Thread(target=_upload_events, daemon=True).start()

            if SHOW_WINDOW:
                for t in tracks:
                    l, t_, r, b = (int(v) for v in t.to_ltrb())
                    cv2.rectangle(frame, (l, t_), (r, b), (255, 0, 0), 2)
                    cv2.putText(frame, f"ID {t.track_id}", (l, t_ - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                cv2.putText(frame, f"Total: {snap['total']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Trash detector", frame)
                if cv2.waitKey(1) & 0xFF == 27:  # Esc quits
                    break

    cap.release()
    if SHOW_WINDOW:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # The API runs in a background thread so OpenCV windows stay on the main thread (required on macOS).
    server = threading.Thread(
        target=uvicorn.run, kwargs={"app": app, "host": os.getenv("HOST", "127.0.0.1"), "port": 8000}, daemon=True
    )
    server.start()
    detection_loop()
