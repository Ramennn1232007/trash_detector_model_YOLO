import cv2

def initialize_camera():
    """
    Initialize the camera using OpenCV.
    Returns:
        cap (cv2.VideoCapture): The video capture object for the camera.
    Raises:
        ValueError: If the camera could not be opened.
    """
    cap = cv2.VideoCapture(0)  # Open the first available camera (device 0)
    if not cap.isOpened():
        raise ValueError("Could not open the camera.")
    return cap
