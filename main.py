import cv2
import logging
import os
from fastapi import FastAPI, WebSocket, Request
import uvicorn
from threading import Thread
import asyncio
from pydantic import BaseModel
from detection.yolo_model import load_model
from detection.detection import perform_detection
from tracking.tracking import TrackerManager
from utils.camera import initialize_camera
from utils.alert_system import check_trash_threshold
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import datetime
import random  # For generating mock pH data
from aws_integration import upload_to_s3
from fastapi.middleware.cors import CORSMiddleware

# Set up logging configuration
logging.basicConfig(
    filename='detection_log.log',
    level=logging.INFO,
    format='%(asctime)s,INFO:%(message)s'  # Ensure consistent logging format for Lambda parsing
)

# Load environment variables from .env file
load_dotenv()

# Load environment variables
MODEL_PATH = os.getenv("MODEL_PATH", "models/best_one_class.pt")
TRASH_THRESHOLD = int(os.getenv("TRASH_THRESHOLD", 1))
S3_BUCKET = os.getenv("S3_BUCKET")

# Global variable to store the total objects detected
total_objects_detected = 0

app = FastAPI()

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for error handling
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return JSONResponse(status_code=500, content={"detail": str(e)})

# Model for pH data logging
class pHData(BaseModel):
    pH: float

# Model for trash count data logging
class TrashData(BaseModel):
    count: int

# Endpoint to log pH data
@app.post("/log-ph")
def log_ph(data: pHData):
    logging.info(f"pH data received: {data.pH}")
    return {"status": "success", "data": data}

# Endpoint to log trash count data
@app.post("/log-trash-count")
def log_trash_count(data: TrashData):
    logging.info(f"Received trash count data: {data.count}")
    return {"status": "success", "data": data}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

def get_current_trash_count():
    global total_objects_detected
    return total_objects_detected

@app.get("/")
def read_root():
    return {"message": "Welcome to the Trash Detection API"}

@app.get("/status")
def get_status():
    return {"status": "Monitoring"}

@app.get("/trash-count")
def get_trash_count():
    return {"count": get_current_trash_count()}

@app.websocket("/ws/trash-count")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        trash_count = get_current_trash_count()
        await websocket.send_json({"count": trash_count})
        await asyncio.sleep(5)

def generate_mock_ph_value():
    """Generate a random pH value between 6.5 and 8.5."""
    return round(random.uniform(6.5, 8.5), 2)

def detection_loop():
    global total_objects_detected

    try:
        model = load_model(MODEL_PATH)
    except Exception as e:
        logging.error(f"Failed to load model from {MODEL_PATH}: {e}")
        return

    try:
        cap = initialize_camera()
    except Exception as e:
        logging.error(f"Failed to initialize camera: {e}")
        return

    tracker_manager = TrackerManager()
    counted_ids = set()

    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                logging.warning("Failed to read frame from camera")
                continue  # Skip this loop iteration if frame is not captured

            # Perform detection and edge detection
            detections, edges = perform_detection(model, frame)
            tracked_objects = tracker_manager.update(detections, frame)

            for track in tracked_objects:
                track_id = track.track_id

                if track_id not in counted_ids:
                    counted_ids.add(track_id)
                    total_objects_detected += 1
                    # Log the detection event
                    logging.info(f"Detection: Track ID {track_id}, Total Trash Detected: {total_objects_detected}")

                bbox = track.to_tlbr()
                cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)
                cv2.putText(frame, f'Track ID: {track_id}', (int(bbox[0]), int(bbox[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            # Generate and log mock pH data
            ph_value = generate_mock_ph_value()
            logging.info(f"pH data received: {ph_value}")

            # Check if the total detected trash count exceeds the threshold
            if check_trash_threshold(total_objects_detected):
                logging.info(f"Alert triggered: {total_objects_detected} item(s) of trash detected, threshold was {TRASH_THRESHOLD}")
                total_objects_detected = 0  # Optionally reset the count after sending the alert

                # When the trash threshold is exceeded, upload the log file to S3
                local_file = "detection_log.log"
                s3_file = f"logs/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_log.log"

                # Upload the file to S3
                if local_file and S3_BUCKET and s3_file:
                    success = upload_to_s3(local_file, S3_BUCKET, s3_file)
                    if success:
                        logging.info(f"Successfully uploaded {local_file} to {s3_file}")
                    else:
                        logging.error(f"Failed to upload {local_file} to S3.")
                else:
                    logging.error("Missing required parameters for S3 upload.")

            # Display the edges
            cv2.imshow('Edges', edges)

            # Display the original frame with detections
            cv2.putText(frame, f"Total Trash Detected: {total_objects_detected}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Webcam', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break
        except Exception as e:
            logging.error(f"An error occurred during detection: {e}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detection_thread = Thread(target=detection_loop)
    detection_thread.start()

    uvicorn.run(app, host="0.0.0.0", port=8000)
