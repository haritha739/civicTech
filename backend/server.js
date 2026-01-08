
const express = require("express");
const cors = require("cors");
const multer = require("multer");
const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs");
const path = require("path");


const app = express();
const uploadDir = path.join(__dirname, "uploads");
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

const upload = multer({ dest: uploadDir });

app.use(cors());
app.use(express.json());

// TEMP DATABASE (for now)
let complaints = [];

// SUBMIT COMPLAINT (Report Issue page)
app.post("/api/complaint", (req, res) => {
  const id = "CIV-" + Date.now();

  const complaint = {
    id,
    category: req.body.category,
    description: req.body.description,
    priority: req.body.priority || "NORMAL",
    status: "SUBMITTED",
    severity: req.body.priority === "EMERGENCY" ? "CRITICAL" : "NORMAL",
    createdAt: new Date()
  };

  complaints.push(complaint);

  res.json({
    message: "Complaint submitted successfully",
    id: complaint.id
  });
});

// TRACK COMPLAINT
app.get("/api/complaint/:id", (req, res) => {
  const complaint = complaints.find(c => c.id === req.params.id);

  if (!complaint) {
    return res.status(404).json({ error: "Complaint not found" });
  }

  res.json(complaint);
});

// ADMIN DASHBOARD
app.get("/api/admin/complaints", (req, res) => {
  res.json(complaints);
});
app.post("/api/ai-verify", upload.single("image"), async (req, res) => {
  try {
    const { category } = req.body;

    if (!req.file || !category) {
      return res.status(400).json({ error: "Image and category required" });
    }

    const formData = new FormData();
    formData.append("image", fs.createReadStream(req.file.path));
    formData.append("category", category);

    const aiRes = await axios.post(
      "http://localhost:8001/verify",
      formData,
      { headers: formData.getHeaders() }
    );

    fs.unlinkSync(req.file.path);

    res.json(aiRes.data);

  } catch (err) {
    console.error(err.message);
    res.status(500).json({ error: "AI verification failed" });
  }
});
app.get("/", (req, res) => {
  res.json({
    status: "Backend running",
    services: {
      complaints: "OK",
      ai_verification: "OK"
    }
  });
});

app.listen(5000, () => {
  console.log("✅ Backend running at http://localhost:5000");
});
