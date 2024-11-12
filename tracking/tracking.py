from tracking.deepsort import initialize_tracker

class TrackerManager:
    def __init__(self):
        self.tracker = initialize_tracker()

    def update(self, detections, frame):
        # Convert detections to the required format
        dets = []
        for bbox, confidence, class_id in zip(detections.xyxy.cpu().numpy(), detections.conf.cpu().numpy(), detections.cls.cpu().numpy()):
            dets.append((bbox, confidence, class_id))

        # Update the tracker
        return self.tracker.update_tracks(dets, frame=frame)
