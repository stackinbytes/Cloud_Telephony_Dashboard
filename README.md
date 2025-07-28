# 📞 Claritel – Cloud Telephony Dashboard

Claritel is a full-stack application built with **FastAPI** (Python) and **React** (JavaScript) that simulates a cloud telephony dashboard. It supports basic call center functionality such as logging calls, initiating actions like transfer or hangup, and simulating audio playback. Great for testing, prototypes, or educational demos.

---

## ✨ Features

- 📋 Live call log table  
- ✅ Call initiation via frontend  
- 🔄 Status updates: ringing, in-progress, completed, etc.  
- 🔁 Transfer & 🔴 Hangup simulation  
- 🔊 Play audio simulation  
- 🔍 Filter calls by status  
- 🔃 Sort by time (newest/oldest)  
- 🔎 Search by number  
- 🚀 Auto-refreshing UI  

---

## 🧱 Tech Stack

| Layer     | Tech Stack                        |
|-----------|-----------------------------------|
| Frontend  | React, Tailwind CSS, Axios        |
| Backend   | FastAPI, Pydantic, SQLAlchemy     |
| Database  | SQLite (swappable)                |
| Tooling   | Vite, npm, Uvicorn                |

---

## 📂 Folder Structure

<pre>

.
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── database.py              # Database connection setup
│   ├── models/                  # SQLAlchemy models
│   ├── schemas/                 # Pydantic schemas
│   └── routes/                  # API route handlers
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CallTable.jsx    # Displays live call logs
│   │   │   └── CallForm.jsx     # Form to initiate calls
│   │   ├── App.jsx              # Main application component
│   │   └── index.css            # Tailwind CSS styles
│   ├── public/                  # Static assets
│   ├── tailwind.config.js       # Tailwind config
│   └── vite.config.js           # Vite config

</pre>

---

## 🚀 Getting Started

### 🖥️ Frontend Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install frontend dependencies
npm install

# Start the React development server
npm run dev

# App runs at: http://localhost:5173
```

### ⚙️ Backend Setup
```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload

# API runs at: http://127.0.0.1:8000
```

### Screenshot
<img width="1879" height="761" alt="image" src="https://github.com/user-attachments/assets/07eaf03d-d44d-428d-b3f5-7606e0047932" />

## ⚙️ Functionality Overview

Claritel simulates key operations of a cloud telephony dashboard, combining call tracking and simulated call actions in a seamless UI backed by a RESTful API.

---

### 📞 Call Management

- **Initiate Call**
  - Via the frontend form
  - Creates a new call log in the system
  - Default status: `queued`

- **View Call Log**
  - Displays all past and ongoing calls in a table
  - Shows: from/to number, status, start time, and duration

- **Filter by Status**
  - Dropdown to view calls with a specific status (e.g., `in_progress`, `completed`)

- **Sort by Start Time**
  - Sort calls ascending or descending by timestamp

- **Search by Number**
  - Real-time filtering of calls by matching either from or to number

- **Auto-Refresh**
  - Call table refreshes every 10 seconds to reflect new activity

---

### 🎛 Simulated Call Actions

- **▶️ Play Audio**
  - Sends a request to simulate playing audio for a call
  - Accepts a URL to the audio file

- **🔁 Transfer**
  - Prompt for a target number
  - Simulates transferring the call to the new number

- **🔴 Hangup**
  - Simulates call hangup
  - Updates the call status to `completed`
  - Sets the call duration from start time to hangup time
