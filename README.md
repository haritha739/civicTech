
⚙️ Installation & Setup (From Scratch)

🔹 Prerequisites

* Python 3.9+
* VS Code
* Internet connection (for model download)
 ▶️ How to Run the Project 
✅ Step 1: Open Project in VS Code

* Open **VS Code**
* Select **Open Folder**
* Choose `civic-admin`
✅ Step 2: Start Backend (AI Server)

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
 ✅ Step 3: Start Frontend

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

## 📌 Important Notes

* Frontend and Backend **must run simultaneously**
* Do **not** open HTML files directly (`file://`)
* Always use `http://localhost:5500`

