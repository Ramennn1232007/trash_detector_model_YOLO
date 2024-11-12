import cv2

def perform_detection(model, frame):
    # Convert the frame to grayscale (necessary for edge detection)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform Canny edge detection
    edges = cv2.Canny(gray_frame, 100, 200)

    # Now, use the model to perform object detection on the original frame
    results = model(frame)
    if results:
        return results[0].boxes, edges
    return [], edges
