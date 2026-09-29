"""Loads the trained checkpoint.

The checkpoints in models/ were trained with the THU-MIG YOLOv10 fork (ultralytics 8.1.34),
which exposes a YOLOv10 class. See requirements.txt for the pinned install.
"""


def load_model(model_path):
    try:
        from ultralytics import YOLOv10
        return YOLOv10(model_path)
    except ImportError:
        from ultralytics import YOLO
        return YOLO(model_path)
