from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from main import run_pipeline

app = FastAPI(title="Road Infra API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/video")
async def detect(file: UploadFile = File(...)):
    # read bytes, run your OpenCV / Roboflow / YOLO pipeline
    data = await file.read()
    # ... process ...
    return JSONResponse({"predictions": []})