Perfect 👍
Here is a **clean, professional `README.md`** you can **directly copy-paste** into your project root (`civic-admin/README.md`).
This is **hackathon-ready**, clear for judges, and explains everything properly.

---

# 🏙️ CivicAI – AI-Verified Civic Complaint System

CivicAI is an **AI-powered civic issue reporting platform** that enables citizens to report public infrastructure and safety issues with **image evidence, location data, and automated AI verification**.
The system verifies complaints using computer vision and intelligently categorizes and prioritizes them for faster civic action.

---

## 🚀 Key Features

* 📸 **Image-based complaint reporting**
* 🤖 **AI verification using YOLOv8**
* 📍 **Location capture**

  * Use **current GPS location**
  * OR manually **add address** (state, city, street, pincode)
* ⚠️ **Severity classification** (LOW / MEDIUM / HIGH)
* 🏷️ **Automatic issue categorization**
* 🔄 **Manual review fallback for uncertain cases**
* 🧠 **Duplicate & fake complaint reduction**
* 🖥️ Clean and user-friendly UI

---

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript (Vanilla)
* Browser Geolocation API
* Google Maps (for location preview)
* Python HTTP Server (local development)

### Backend

* **FastAPI** (Python)
* **Uvicorn** (ASGI Server)
* **YOLOv8 (Ultralytics)** – Object Detection
* OpenCV
* NumPy

### AI / ML

* YOLOv8 pretrained model
* Heuristic image analysis for civic issues
* Confidence-based verification logic

---

## 📂 Project Structure

```
civic-admin/
│
├── civic-ai-verification/        # Backend (FastAPI + AI)
│   ├── main.py
│   └── uploads/
│
├── frontend/                     # Frontend
│   ├── report.html
│   ├── track.html
│   ├── admin.html
│   └── lang.js
│
└── README.md
```

---

## ⚙️ Installation & Setup (From Scratch)

### 🔹 Prerequisites

* Python 3.9+
* VS Code
* Internet connection (for model download)

---

## ▶️ How to Run the Project (IMPORTANT)

### ✅ Step 1: Open Project in VS Code

* Open **VS Code**
* Select **Open Folder**
* Choose `civic-admin`

---

### ✅ Step 2: Start Backend (AI Server)

Open **Terminal 1** in VS Code:

```powershell
cd civic-ai-verification
python -m pip install fastapi uvicorn ultralytics opencv-python numpy
python -m uvicorn main:app --reload
```

✔ Backend runs on:

```
http://127.0.0.1:8000
```

✔ API Docs:

```
http://127.0.0.1:8000/docs
```

---

### ✅ Step 3: Start Frontend

Open **Terminal 2** in VS Code:

```powershell
cd frontend
python -m http.server 5500
```

✔ Frontend runs on:

```
http://localhost:5500/report.html
```

---

## 🧪 How It Works

1. User uploads an image of a civic issue
2. User selects category
3. User provides **location OR address**
4. Image is sent to AI backend
5. AI detects objects and verifies issue
6. System returns:

   * Verification status
   * Confidence score
   * Severity level
7. Complaint is auto-approved or sent for manual review

---

## 📊 Sample AI Response

```json
{
  "verified": true,
  "confidence": 0.88,
  "severity": "HIGH",
  "detected_objects": ["car", "person"],
  "status": "AUTO_VERIFIED"
}
```

---

## 🏁 Use Cases

* Road accidents
* Fire hazards
* Garbage overflow
* Potholes
* Broken streetlights
* Drainage issues
* Public safety hazards

---

## 🎯 Why CivicAI?

* Reduces fake complaints
* Speeds up civic response
* Improves transparency
* Uses AI for real-world impact
* Scalable for smart cities

---

## 🧩 Future Enhancements

* Citizen login & complaint history
* Admin dashboard with analytics
* Complaint tracking with status updates
* Government department integration
* Mobile app version

---

## 👨‍💻 Developed For

* Hackathons
* Smart City solutions
* Civic-tech innovation challenges
* AI for Social Good initiatives

---

## 📌 Important Notes

* Frontend and Backend **must run simultaneously**
* Do **not** open HTML files directly (`file://`)
* Always use `http://localhost:5500`

---

## 🏆 Project Status

✅ **Completed**
✅ **End-to-End Functional**
✅ **Hackathon Ready**

---

If you want, next I can help you with:

* 🎤 **Hackathon demo explanation**
* 📊 **PPT slides**
* 🧠 **Architecture diagram**
* 📝 **Problem statement & solution write-up**

Just tell me 👍
