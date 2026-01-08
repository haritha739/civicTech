from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
from datetime import datetime
from ultralytics import YOLO
import shutil
import uuid
import os
import cv2
import numpy as np

# --------------------
# App init
# --------------------
app = FastAPI(title="AI Civic Issue Verification Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "AI service running"}

# --------------------
# YOLO model
# --------------------
model = YOLO("yolov8n.pt")
# In-memory complaint storage
complaints = {}

# --------------------
# Upload directory
# --------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------------------
# CIVIC HEURISTIC FUNCTIONS
# (Pre-screening only, NOT final verification)
# --------------------
def edge_density(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(img, 100, 200)
    return edges.mean() / 255

def garbage_signal(image_path):
    return edge_density(image_path) > 0.08

def pothole_signal(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    large = [c for c in contours if cv2.contourArea(c) > 500]
    return len(large) > 0

def open_drain_signal(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(img, 50, 150)
    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180,
        threshold=100,
        minLineLength=120,
        maxLineGap=10
    )
    return lines is not None

def broken_streetlight_signal(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return img.mean() < 70

# --------------------
# YOLO CATEGORY RULES
# --------------------
YOLO_RULES = {
    "accident": {
        "allowed": ["car", "bus", "truck", "motorcycle", "bicycle", "person"],
        "min_conf": 0.6
    },
    "fire": {
        "allowed": ["fire", "smoke"],
        "min_conf": 0.6
    }
}

# --------------------
# VERIFY ENDPOINT
# --------------------
@app.post("/verify")
async def verify_image(
    image: UploadFile = File(...),
    category: str = Form(...)
):
    category = category.strip().lower()

    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}.jpg"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # --------------------
    # YOLO-BASED CATEGORIES
    # --------------------
    if category in YOLO_RULES:
        rules = YOLO_RULES[category]
        allowed = rules["allowed"]
        min_conf = rules["min_conf"]

        detected = []
        max_conf = 0.0

        results = model(file_path)
        for r in results:
            for box in r.boxes:
                conf = float(box.conf)
                cls = model.names[int(box.cls)]

                if conf >= min_conf and cls in allowed:
                    detected.append(cls)
                    max_conf = max(max_conf, conf)

        os.remove(file_path)

        verified = False

        if category == "accident":
            vehicles = {"car", "bus", "truck", "motorcycle", "bicycle"}
            has_vehicle = any(d in vehicles for d in detected)
            has_person = "person" in detected

            if has_vehicle and (has_person or len(detected) >= 2):
                verified = True

        if category == "fire" and detected:
            verified = True

        severity = (
            "HIGH" if max_conf > 0.75 else
            "MEDIUM" if max_conf > 0.5 else
            "LOW"
        )

        return {
            "verified": verified,
            "confidence": round(max_conf, 2),
            "severity": severity,
            "detected_objects": detected,
            "status": "AUTO_VERIFIED" if verified else "MANUAL_REVIEW"
        }

    # --------------------
    # CIVIC HEURISTIC CATEGORIES
    # --------------------
    signal = False
    reason = ""

    if category == "garbage":
        signal = garbage_signal(file_path)
        reason = "High visual clutter detected"

    elif category in ["pothole", "manhole", "road_damage"]:
        signal = pothole_signal(file_path)
        reason = "Irregular dark surface patterns detected"

    elif category in ["open_drain", "drainage_block"]:
        signal = open_drain_signal(file_path)
        reason = "Linear cavity-like edges detected"

    elif category == "broken_streetlight":
        signal = broken_streetlight_signal(file_path)
        reason = "Low illumination detected"

    else:
        os.remove(file_path)
        return {
            "verified": False,
            "confidence": 0.0,
            "severity": "LOW",
            "detected_objects": [],
            "status": "INVALID_CATEGORY"
        }

    os.remove(file_path)

    return {
        "verified": False,
        "confidence": 0.4 if signal else 0.0,
        "severity": "MEDIUM" if signal else "LOW",
        "detected_objects": [],
        "status": "MANUAL_REVIEW",
        "note": "AI pre-screening only; human verification required",
        "signal_reason": reason
    }