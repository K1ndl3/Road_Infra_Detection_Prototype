# so we need a clear pipeline
import os
import cv2
import numpy as np
from ultralytics import YOLO
from dotenv import load_dotenv

from inference_sdk import InferenceHTTPClient
load_dotenv()

api = os.getenv("ROBOFLOW_API_KEY")

def printResult(result):
    obj = result["predictions"]
    size = len(obj)
    for i in range(0, size, 1):
        type = obj[i]["class"]
        confidence_level = obj[i]["confidence"]
        print(type, confidence_level)
    return 

"""
pipeline:
    1) video ingest
        - use cv2 to load the video
            videoCapture()
    2) breaking up into frames
        - for loop 
        - use .read()
        - add frames into vector
    3a) load a model using yolo
    3b) feed frames into model
        - for every frame, add to model

    4) averate output from model
        - deconstruct the model object and aggregate score, find average
    5) display model
        - display average
"""

#1 video ingest
capture = cv2.VideoCapture("./footage1.webm")
if (capture.isOpened() == False):
    print("failed to open")
print("video loaded succesfully")

#2 frame capture
frames = []
for i in range(0,30,1):
    success, frame = capture.read()

    if not success:
        break;
    frames.append(frame)
capture.release()


#3 load model
model = YOLO("yolo26n.pt")

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key= api
)
results = []
for frame in frames:
    result = client.infer(
    frame,
    model_id="pothole-detection-i00zy-qvchi-qllyn/1"
)
    results.append(result)

for result in results:
    printResult(result)

#for result in results:
    #print(result)

