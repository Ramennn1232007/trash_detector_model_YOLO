# Trash Detector (YOLOv10 + DeepSORT)

Counts visible litter in a camera feed or recorded video. Each frame goes through a YOLOv10 detector, a DeepSORT tracker gives every object an ID, and each confirmed ID is counted once. A small FastAPI server exposes the count, and a React page shows it live.

> **Status: v0.2, working prototype.** Detection accuracy has only been measured on the TACO validation split (see Results). It has not yet been tested on field data or compared with hand counts, and there is no map yet. See Roadmap.

## How it works

```
camera / video file
      │
      ▼
YOLOv10 detector  ──►  DeepSORT tracker  ──►  count each confirmed track once
                                                   │
                         detections.jsonl  ◄───────┤
                         FastAPI /trash-count ◄────┤
                         WhatsApp alert (optional) ◄┘
```

## Results so far

Metrics read from the saved checkpoints. These are **validation-split** numbers from training, so they are optimistic; no held-out test set has been scored yet.

| Model file | Base | Training data | Classes | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|---|---|---|
| `models/best_one_class.pt` (default) | YOLOv10n, 50 epochs | TACO (Roboflow export) | 1: trash | 0.56 | 0.42 | 0.41 | 0.25 |
| `models/best_4000_img_train3.pt` | YOLOv10s, 132 epochs | TACO (Roboflow export) | 18 TACO classes | 0.70 | 0.42 | 0.46 | 0.35 |

What this means: at the default setting the model finds roughly 4 in 10 labeled items. Counts from this system are therefore **lower bounds**.

## Install

Python 3.10 or newer.

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # then edit .env
```

The checkpoints were trained with the [THU-MIG YOLOv10 fork](https://github.com/THU-MIG/yolov10), which `requirements.txt` installs.

## Run it live

```bash
python main.py
```

- `SHOW_WINDOW=true` in `.env` opens a video window (press Esc to quit). Leave it `false` on a headless device.
- `CAMERA_SOURCE=0` is the first webcam; set it to a file path or stream URL to run on video.
- API: `GET /trash-count`, `GET /status`, `GET /health`, WebSocket `/ws/trash-count`.
- Every counted item is appended to `detections.jsonl` (time, track ID, class, confidence, box).

Dashboard:

```bash
cd frontend
cp .env.example .env
npm install
npm start
```

## Measure counting accuracy

Record short clips, have two people agree on the number of unique items in each, and put them in `hand_counts.csv`:

```
clip,count
clip01.mp4,7
clip02.mp4,3
```

Then:

```bash
python count_video.py clips/*.mp4 --hand-counts hand_counts.csv
```

It prints mean absolute error and percent error and writes `results/count_eval.csv`.

## Known limitations

- Trained only on TACO, which is mostly close-up photos of litter on the ground. Expect lower accuracy on other viewpoints (fixed cameras, water, drones).
- The confidence threshold (0.25) is the training default, not yet tuned on a precision-recall curve.
- No location data yet, so no map.
- The pH endpoint accepts readings from a real sensor; no sensor is connected, and the code does not generate pH values.

## Roadmap

1. Pick the deployment setting and write the one-sentence claim.
2. Retrain with splits made before augmentation, plus a held-out test set.
3. Collect and label 300 to 500 images from the real setting; report field accuracy.
4. Measure counting error on 10 to 20 hand-counted clips.
5. Add GPS to each detection and build a normalized heatmap (items per 100 m surveyed).
6. Partner with a cleanup group and measure before/after.

## Changelog

**v0.2**
- Fixed: tracker received `x1,y1,x2,y2` boxes where DeepSORT expects `left,top,width,height`.
- Fixed: tentative (unconfirmed) tracks were counted.
- Fixed: total count reset to 0 after every alert.
- Fixed: alert threshold had two different defaults (1 and 5).
- Removed: randomly generated pH values that were logged as sensor readings.
- Removed: unused Canny edge detection.
- Alerts and S3 uploads now run off the video thread; windows are optional; camera loss stops cleanly.
- Added `count_video.py` for count-error evaluation, `detections.jsonl` event log, `.env.example`, pinned requirements.

## License

The YOLOv10 code and the weights derived from it are AGPL-3.0. This repository is distributed under AGPL-3.0 as well; see `LICENSE`.

## Credits

Built by [add names and roles]. Dataset: [TACO](http://tacodataset.org) (Proença and Simões, 2020).
