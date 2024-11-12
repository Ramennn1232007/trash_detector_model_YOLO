from ultralytics import YOLOv10

def load_model(model_path):
    return YOLOv10(model_path)
