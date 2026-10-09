"""Local inference pipeline for the RD2022 crack/pothole model (best.pt)."""
import os

import cv2
from ultralytics import YOLO

WEIGHTS_PATH = os.getenv(
    "RD2022_WEIGHTS",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "best.pt"),
)
OUTPUT_DIR = os.path.join("output", "rd2022")
MAX_FRAMES = 30
CONFIDENCE_THRESHOLD = 0.25

CLASS_NAMES = {
    0: "Longitudinal Cracks",
    1: "Transverse Cracks",
    2: "Alligator Cracks",
    3: "Potholes",
}

_model = None


def get_model():
    global _model
    if _model is None:
        if not os.path.isfile(WEIGHTS_PATH):
            raise FileNotFoundError(f"RD2022 weights not found: {WEIGHTS_PATH}")
        _model = YOLO(WEIGHTS_PATH)
    return _model


def _color_for_confidence(confidence):
    if confidence < 0.3:
        return (0, 0, 255)
    if confidence <= 0.7:
        return (255, 0, 0)
    return (0, 255, 0)


def predictions_from_result(result):
    predictions = []
    boxes = result.boxes
    if boxes is None:
        return predictions

    names = result.names or CLASS_NAMES
    for box in boxes:
        x, y, width, height = box.xywh[0].tolist()
        class_id = int(box.cls[0].item())
        confidence = float(box.conf[0].item())
        label = names.get(class_id, CLASS_NAMES.get(class_id, str(class_id)))
        predictions.append({
            "class_id": class_id,
            "class": label,
            "confidence": confidence,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
        })
    return predictions


def draw_predictions(frame, predictions, index):
    for pred in predictions:
        width = pred["width"]
        height = pred["height"]
        x_start = int(pred["x"] - width / 2)
        y_start = int(pred["y"] - height / 2)
        x_end = int(pred["x"] + width / 2)
        y_end = int(pred["y"] + height / 2)
        confidence = pred["confidence"]
        label = f"{pred['class']} {confidence:.2f}"
        color = _color_for_confidence(confidence)

        cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), color, 2)
        cv2.putText(frame, label, (x_start, max(y_start - 8, 16)), 0, 0.6, (0, 0, 0), 2)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cv2.imwrite(os.path.join(OUTPUT_DIR, f"frame_{index}.jpg"), frame)
    return frame


def print_predictions(predictions, frame_num):
    for pred in predictions:
        print(pred["class"], f"{pred['confidence']:.2f}", "frame:", frame_num)


def run_rd2022_pipeline(source, max_frames=MAX_FRAMES):
    """Read a video, run local RD2022 detection, and return annotated frames."""
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        print("failed to open")
        return []
    print("video loaded succesfully")

    frames = []
    for _ in range(max_frames):
        success, frame = capture.read()
        if not success:
            break
        frames.append(frame)
    capture.release()

    model = get_model()
    annotated = []
    for index, frame in enumerate(frames):
        result = model.predict(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)[0]
        predictions = predictions_from_result(result)
        print_predictions(predictions, index)
        annotated_frame = draw_predictions(frame.copy(), predictions, index)
        annotated.append({
            "frame": annotated_frame,
            "predictions": predictions,
        })

    return annotated


if __name__ == "__main__":
    run_rd2022_pipeline("./pothole2.webm")
