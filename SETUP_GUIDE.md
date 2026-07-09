# HarvestIQ - Setup & Build Guide

## Project Overview
This is **HarvestIQ**, a premium farm intelligence platform with a React frontend and Flask backend that uses machine learning to predict crop yields and provide agricultural advice.

### Architecture
```
crop-yield-bot/
├── frontend/          (React + Vite)
│   ├── src/          (React components)
│   ├── package.json  (Node dependencies)
│   └── vite.config.js
├── backend/          (Flask + Python)
│   ├── app.py        (API server)
│   ├── requirements.txt (Python dependencies)
│   └── data/         (Training data)
└── model.pkl         (Trained ML model - REQUIRED)
```

## Prerequisites
- **Node.js** (v16+) and npm
- **Python** (v3.8+) and pip
- **model.pkl** file in the backend directory (trained model file)

## Setup Instructions

### 1. Backend Setup (Flask)

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt
```

**Dependencies:**
- pandas - Data manipulation
- numpy - Numerical computing
- scikit-learn - Machine learning
- Flask - Web framework
- flask-cors - Cross-Origin Resource Sharing
- httpx - HTTP client

### 2. Frontend Setup (React + Vite)

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Verify installation
npm list
```

**Main Dependencies:**
- React 19.2.5 - UI framework
- Vite 8.0.10 - Build tool & dev server
- ESLint - Code quality

## Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```
- Runs on: `http://localhost:5000`
- Flask debug mode enabled
- CORS enabled for frontend access

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
- Runs on: `http://localhost:5173` (Vite default)
- Hot Module Replacement (HMR) enabled
- Auto-refresh on code changes

Notes:
- Vite's default dev port is `5173`, but the dev server may run on a different port (for example `3000`) if the environment `PORT` is set or another service is already using `5173`.
- To explicitly run the frontend on a particular port, set the `PORT` environment variable for the session before starting Vite (examples below).

PowerShell (set port for current session):
```powershell
$env:PORT = '5173'
npm run dev
```

PowerShell (pass through to Vite):
```powershell
npm run dev -- --port 5173
```

Command Prompt (cmd.exe):
```cmd
set PORT=5173&& npm run dev
```

### Production Build

**Build Frontend:**
```bash
cd frontend
npm run build
```
- Generates: `frontend/dist/` folder
- Optimized, minified production assets
- Ready to deploy

**Backend:**
- The Flask app auto-reloads in debug mode
- For production, set `debug=False` in `app.py` line 121

## API Endpoints

### 1. Crop Yield Prediction
**POST** `/api/predict`

**Request Body:**
```json
{
  "season": "summer",
  "crop_type": "wheat",
  "soil_type": "loam",
  "temperature": 25.5,
  "rainfall": 600,
  "humidity": 70,
  "nitrogen": 100,
  "phosphorus": 50,
  "potassium": 40
}
```

**Response:**
```json
{
  "success": true,
  "yield_ton_per_ha": 4.56,
  "details": {
    "season": "summer",
    "crop_type": "wheat",
    "soil_type": "loam",
    "temperature": 25.5,
    "rainfall": 600,
    "humidity": 70
  }
}
```

### 2. Chatbot Assistance
**POST** `/api/chat`

**Request Body:**
```json
{
  "message": "What's the best crop for loam soil?"
}
```

**Response:**
```json
{
  "success": true,
  "message": "What's the best crop for loam soil?",
  "reply": "For fertile loam soil with moderate rainfall, wheat and maize often give good yields..."
}
```

## Environment Configuration

### Backend (.env file - Optional)
Create `backend/.env` if needed:
```
FLASK_ENV=development
FLASK_DEBUG=True
MODEL_PATH=model.pkl
PORT=5000
```

Tip: copy the example file:
```bash
cd backend
copy .env.example .env
```

### Frontend (.env file - Optional)
Create `frontend/.env.local` if needed:
```
VITE_API_URL=http://localhost:5000
```

Tip: copy the example file:
```bash
cd frontend
copy .env.example .env.local
```

The frontend is configured to read `VITE_API_URL` at build/dev time. If `VITE_API_URL` is not provided, the code falls back to `http://localhost:5000`.

Example to write the variable from PowerShell (project root):
```powershell
echo VITE_API_URL="http://localhost:5000" > frontend\.env
```

If your backend runs on `http://localhost:3000` instead, set `VITE_API_URL` accordingly.

Update `frontend/src/App.jsx` if you change the API variable name:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'
```

## Important Notes

⚠️ **model.pkl is REQUIRED**: The backend expects a trained ML model file at `backend/model.pkl`. Without it, the prediction endpoint will fail.

The model file should contain:
- Trained ML model
- Label encoders for: season, crop_type, soil_type

## Build Commands Quick Reference

| Command | Purpose |
|---------|---------|
| `npm install` | Install frontend dependencies |
| `npm run dev` | Start frontend dev server |
| `npm run build` | Build optimized frontend |
| `npm run lint` | Check code quality |
| `npm run preview` | Preview production build |
| `pip install -r requirements.txt` | Install backend dependencies |
| `python app.py` | Start Flask backend |

## Troubleshooting

**Issue: Port 5000 already in use**
- Solution: Change port in `backend/app.py` line 121

**Issue: model.pkl not found**
- Solution: Ensure trained model is at `backend/model.pkl`

**Issue: CORS errors in frontend**
- Solution: Backend has CORS enabled, check API URL matches frontend config

**Issue: npm modules not installing**
- Solution: Delete `node_modules` and `package-lock.json`, then run `npm install`

## Next Steps

1. Ensure `model.pkl` is in the backend directory
2. Run backend: `python app.py`
3. In another terminal, run frontend: `npm run dev`
4. Open `http://localhost:5173` in your browser
5. Test the crop yield prediction and chatbot features

---

For more information, refer to:
- [React Documentation](https://react.dev)
- [Vite Documentation](https://vite.dev)
- [Flask Documentation](https://flask.palletsprojects.com)
- [scikit-learn Documentation](https://scikit-learn.org)
