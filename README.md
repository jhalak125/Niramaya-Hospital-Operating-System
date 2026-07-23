# Niramaya: Hospital Operating System

[![Vite](https.img.shields.io/badge/Frontend-React%20%7C%20Vite%20%7C%20TailwindCSS-blue)](https://vitejs.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20Python%203.9+-green)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB%20Atlas-brightgreen)](https://www.mongodb.com/)
[![AI Platform](https://img.shields.io/badge/AI-Vaidya%20AI%20%7C%20Gemini%20%7C%20Groq-purple)](https://groq.com/)

**Niramaya** is an AI-powered healthcare operating platform built for patients, specialist doctors, and healthcare administrators. Featuring instant clinical symptom checking, intelligent lab report file narrations (in English and Hindi), patient appointment scheduling, digital prescription issuance, and administrative financial revenue telemetry.

---

## 🌟 Key Features

- 🏥 **Patient Portal Workspace**: Browse specialist doctor directories, book consultation appointments in Indian Rupees (₹), track appointment statuses, and upload digital payment proofs.
- 🩺 **Doctor Clinical Workspace**: View scheduled appointments, issue electronic prescriptions, add lab tests, submit lab report diagnostics, and access patient clinical history.
- 📊 **Executive Control Console (Admin Dashboard)**: Monitor patient registries, specialist doctor profiles, scheduled consultations, financial billing receipts, and exact system metrics.
- 🤖 **Free AI Health Symptom Checker**: Instant clinical triage and department recommendations based on plain text symptoms — accessible freely without login requirements.
- 🎙️ **Free Vaidya AI File Report Analyzer**: Upload medical lab report PDFs or images to receive automated diagnostic analysis and natural audio narrations in **Hindi (हिंदी)** and **English**.
- 📱 **Fully Responsive Glassmorphic UI**: Optimized across all viewports (Mobile, Tablet, and Desktop) with a modern glassmorphic theme.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons, React Router DOM
- **Backend**: FastAPI (Python), Motor (Async MongoDB Driver), Pydantic v2
- **Database**: Cloud MongoDB Atlas
- **AI Triage & OCR Engine**: Google Gemini API, Groq AI, gTTS (Google Text-to-Speech)
- **Authentication**: JWT Token-based Auth & Role-Based Access Control (RBAC)

---

## 🚀 Getting Started Locally

### Prerequisites
- Python 3.9+
- Node.js v18+ & npm
- MongoDB Atlas cluster URI

### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/venv/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Fill in your MONGODB_URL and API keys in .env
python main.py
```
Backend server will run at `http://localhost:8000`. API docs available at `http://localhost:8000/docs`.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend application will launch at `http://localhost:5173`.

---

## 🚢 Deployment Guide

### Backend Deployment (Render / Railway / Fly.io / Docker)
1. Push this repository to GitHub.
2. Link the repository to your hosting service (e.g. Render Web Service).
3. Set Build Command: `pip install -r backend/requirements.txt`
4. Set Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT` in root or `cd backend && python main.py`
5. Configure Environment Variables from `.env.example`.

### Frontend Deployment (Vercel / Netlify)
1. Link repository to Vercel/Netlify.
2. Root Directory: `frontend`
3. Build Command: `npm run build`
4. Output Directory: `dist`

---

## 👤 Developer & Credits

Designed & Developed with ❤️ by **Jhalak Verma**.
