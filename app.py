from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import base64
import cv2
import os
import tempfile

from rd2022_pipeline import run_rd2022_pipeline

app = FastAPI(title="Road Infra API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    suffix = os.path.splitext(file.filename or "")[1] or ".mp4"
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        annotated = run_rd2022_pipeline(tmp_path)
        frames = []
        for i, item in enumerate(annotated):
            ok, buffer = cv2.imencode(".jpg", item["frame"])
            if not ok:
                continue
            frames.append({
                "index": i,
                "image_base64": base64.b64encode(buffer).decode("utf-8"),
                "predictions": [
                    {
                        "class_id": pred["class_id"],
                        "class": pred["class"],
                        "confidence": pred["confidence"],
                    }
                    for pred in item["predictions"]
                ],
            })

        return {
            "model": "rd2022",
            "classes": [
                "Longitudinal Cracks",
                "Transverse Cracks",
                "Alligator Cracks",
                "Potholes",
            ],
            "frames": frames,
        }
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
