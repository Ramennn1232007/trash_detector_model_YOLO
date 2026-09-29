from tracking.deepsort import initialize_tracker


class TrackerManager:
    def __init__(self):
        self.tracker = initialize_tracker()

    def update(self, boxes, frame, conf_threshold: float = 0.0):
        """Feed YOLO boxes to DeepSORT and return only confirmed tracks.

        deep_sort_realtime expects each detection as ([left, top, width, height], confidence, class).
        YOLO gives x1, y1, x2, y2, so the width and height have to be computed here.
        """
        dets = []
        if boxes is not None and len(boxes):
            for (x1, y1, x2, y2), conf, cls in zip(
                boxes.xyxy.cpu().numpy(), boxes.conf.cpu().numpy(), boxes.cls.cpu().numpy()
            ):
                if conf < conf_threshold:
                    continue
                dets.append(([float(x1), float(y1), float(x2 - x1), float(y2 - y1)], float(conf), int(cls)))

        tracks = self.tracker.update_tracks(dets, frame=frame)
        # Tentative tracks are often one-frame false positives; never count them.
        return [t for t in tracks if t.is_confirmed()]
