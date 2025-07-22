# Github Repo to Postman Collection Generator

A full-stack tool to analyze any public Express.js GitHub repo and generate a downloadable Postman collection, organized by controller.

## ✨ Key Features
- Paste a public GitHub Express.js repo URL
- Clones and analyzes the codebase using Gemini Flash (Google Generative AI)
- Detects endpoints from controllers, routers, DTOs, and main app files
- Organizes endpoints in the Postman collection by controller (each as a folder)
- Download the generated Postman v2.1 collection JSON
- Beautiful React + Tailwind UI with feedback and error handling

## 🛠 Technologies Used
- **Frontend:** React, Tailwind CSS, Vite
- **Backend:** FastAPI (Python), GitPython, google-generativeai (Gemini Flash)

## 🚀 Setup Instructions

### 1. Backend (FastAPI + Gemini Flash)
```bash
cd server
pip install -r requirements.txt
export GEMINI_API_KEY=your-gemini-api-key
uvicorn main:app --reload
```
- The backend will run at http://localhost:8000

### 2. Frontend (React + Tailwind)
```bash
cd client
npm install
npm run dev
```
- The frontend will run at http://localhost:5173

### 3. Usage
- Enter a public GitHub Express.js repo URL in the frontend
- Click "Generate Collection"
- Download the generated Postman collection when ready

---

Built with ❤️ using FastAPI, Gemini Flash, React, and Tailwind CSS.