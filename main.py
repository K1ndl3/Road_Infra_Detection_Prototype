# so we need a clear pipeline
import os
import cv2
import numpy as np
from ultralytics import YOLO
from dotenv import load_dotenv

from inference_sdk import InferenceHTTPClient
load_dotenv()

api = os.getenv("ROBOFLOW_API_KEY")
    

def printResult(result, frame_num):
    obj = result["predictions"]
    size = len(obj)
    for i in range(0, size, 1):
        type = obj[i]["class"]
        confidence_level = obj[i]["confidence"]
        print(type, confidence_level ,"frame: ", frame_num)
    return

"""
    pipeline for showing image with bounding boxes
    use frame.copy() to make a new image copy
    1) build the dimensions + coords for the rectangle
        - x y width and height 
    2) draw the rectangle
        - cv2.rectangle(img, dimension + coords)
    3) label the image
        - cv2.putText(img, string, coords, font, text_size, color, thickness)
    use cv2.imwrite(path_string, copy) to write to an output file
"""
def showBoundBox(frame, result, index):
    pred = result["predictions"]

    for i in pred:
        width = i["width"]
        height = i["height"]
        x = i["x"]
        y = i["y"]
        x_start = int(x - width / 2)
        y_start = int(y - height / 2)

        x_end = int(x + width / 2)
        y_end = int(y + height / 2)

        label = i["class"]
        confidence_level = i["confidence"]

        if (confidence_level < .3):
            color = [0,0,255]
        elif (confidence_level >=.3 and confidence_level <=.7):
            color = [255,0,0]
        else:
            color = [0,255,0]

        cv2.rectangle(frame,[x_start,y_start],[x_end,y_end],color,1)
        cv2.putText(frame, f"Type: {label} {confidence_level}",[x_start,y_end], 0, .6,(0,0,0),2)
    cv2.imwrite(f"./output/frame_{index}.jpg", frame)
    return frame

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
def run_pipeline(source):
    os.makedirs("./output", exist_ok=True)

    #1 video ingest
    capture = cv2.VideoCapture(source)
    if (capture.isOpened() == False):
        print("failed to open")
        return []
    print("video loaded succesfully")

    #2 frame capture
    frames = []
    for i in range(0,60,1):
        success, frame = capture.read()

        if not success:
            break
        frames.append(frame)
    capture.release()

    #3 load model
    model = YOLO("yolo26n.pt")

    client = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key= api
    )
    annotated = []
    i = 0
    for frame in frames:
        result = client.infer(
            frame,
            model_id="pothole-detection-i00zy-qvchi-qllyn/1"
        )
        copy_frame = frame.copy()
        annotated_frame = showBoundBox(copy_frame, result, i)
        printResult(result, i)
        annotated.append(annotated_frame)
        i = i + 1

    return annotated


if __name__ == "__main__":
    run_pipeline("./pothole2.webm")
