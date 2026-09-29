"""Detection + tracking + counting pipeline, shared by the live server and the video evaluator."""
import threading
from dataclasses import dataclass, field

from detection.yolo_model import load_model
from tracking.tracking import TrackerManager


@dataclass
class CountEvent:
    track_id: str
    class_id: int
    class_name: str
    confidence: float
    bbox_ltrb: tuple
    frame_index: int


@dataclass
class CounterState:
    """Thread-safe counters read by the API and written by the detection loop."""
    total: int = 0
    since_last_alert: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def add(self, n: int = 1):
        with self._lock:
            self.total += n
            self.since_last_alert += n

    def reset_alert_window(self):
        with self._lock:
            self.since_last_alert = 0

    def snapshot(self):
        with self._lock:
            return {"total": self.total, "since_last_alert": self.since_last_alert}


class TrashCounter:
    """Runs YOLO on a frame, tracks objects, and counts each confirmed track once."""

    def __init__(self, model_path: str, conf_threshold: float = 0.25):
        self.model = load_model(model_path)
        self.names = getattr(self.model, "names", {0: "trash"})
        self.conf_threshold = conf_threshold
        self.tracker = TrackerManager()
        self.counted_ids = set()
        self.frame_index = 0

    def process(self, frame):
        """Returns (confirmed_tracks, new_count_events) for one frame."""
        results = self.model(frame, conf=self.conf_threshold, verbose=False)
        boxes = results[0].boxes if results else None
        tracks = self.tracker.update(boxes, frame, self.conf_threshold)

        events = []
        for track in tracks:
            if track.track_id in self.counted_ids:
                continue
            self.counted_ids.add(track.track_id)
            class_id = int(track.get_det_class()) if track.get_det_class() is not None else -1
            conf = track.get_det_conf()
            events.append(CountEvent(
                track_id=str(track.track_id),
                class_id=class_id,
                class_name=self.names.get(class_id, "unknown"),
                confidence=round(float(conf), 3) if conf is not None else -1.0,
                bbox_ltrb=tuple(round(float(v), 1) for v in track.to_ltrb()),
                frame_index=self.frame_index,
            ))
        self.frame_index += 1
        return tracks, events
