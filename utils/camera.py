import cv2


def initialize_camera(source="0"):
    """Open a webcam by index ("0", "1", ...) or a video file / stream URL."""
    src = int(source) if str(source).isdigit() else source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        raise ValueError(f"Could not open camera or video source: {source}")
    return cap
