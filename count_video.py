"""Count trash in recorded video clips so the system's count can be compared with a hand count.

Usage:
    python count_video.py clips/*.mp4 --hand-counts hand_counts.csv

hand_counts.csv has two columns: clip,count  (clip = file name, count = unique items two people agreed on).
Writes results/count_eval.csv and prints mean absolute error and percent error.
"""
import argparse
import csv
import os
import time

import cv2

from pipeline import TrashCounter


def count_clip(path, model_path, conf):
    counter = TrashCounter(model_path, conf)
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise ValueError(f"Could not open {path}")
    frames, start = 0, time.time()
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        counter.process(frame)
        frames += 1
    cap.release()
    elapsed = time.time() - start
    return len(counter.counted_ids), frames, frames / elapsed if elapsed else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clips", nargs="+")
    ap.add_argument("--model", default="models/best_one_class.pt")
    ap.add_argument("--conf", type=float, default=0.25)
    ap.add_argument("--hand-counts", help="CSV with columns clip,count")
    ap.add_argument("--out", default="results/count_eval.csv")
    args = ap.parse_args()

    truth = {}
    if args.hand_counts:
        with open(args.hand_counts) as f:
            truth = {row["clip"]: int(row["count"]) for row in csv.DictReader(f)}

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    rows, abs_errors, pct_errors = [], [], []
    for clip in args.clips:
        name = os.path.basename(clip)
        predicted, frames, fps = count_clip(clip, args.model, args.conf)
        actual = truth.get(name)
        row = {"clip": name, "predicted": predicted, "hand_count": actual, "frames": frames, "fps": round(fps, 1)}
        if actual is not None:
            row["abs_error"] = abs(predicted - actual)
            abs_errors.append(row["abs_error"])
            if actual > 0:
                pct_errors.append(100 * row["abs_error"] / actual)
        rows.append(row)
        print(row)

    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["clip", "predicted", "hand_count", "abs_error", "frames", "fps"])
        w.writeheader()
        w.writerows(rows)

    if abs_errors:
        print(f"\nClips with hand counts: {len(abs_errors)}")
        print(f"Mean absolute error: {sum(abs_errors) / len(abs_errors):.2f} items per clip")
    if pct_errors:
        print(f"Mean percent error: {sum(pct_errors) / len(pct_errors):.1f}%")
    print(f"Saved {args.out}")


if __name__ == "__main__":
    main()
