# HarvestIQ - Application Summary

## What is This Application?

This is **HarvestIQ**, a premium farm intelligence system that helps farmers predict crop yields and get agricultural advice using machine learning and AI.

### Key Features
1. **Crop Yield Prediction** - Predicts harvest yields based on:
   - Season (summer, winter, etc.)
   - Crop type (wheat, maize, paddy, etc.)
   - Soil type (loam, sandy, clay, etc.)
   - Environmental factors (temperature, rainfall, humidity)
   - Soil nutrients (nitrogen, phosphorus, potassium)

2. **AI Chatbot Assistant** - Provides farming advice on:
   - Best crops for specific soil conditions
   - Fertilizer recommendations
   - Irrigation techniques
   - Troubleshooting low yields
   - General farming queries

## Technology Stack

### Frontend
- **React 19.2.5** - UI framework for interactive components
- **Vite 8.0.10** - Ultra-fast build tool with dev server
- **ESLint** - Code quality and style checking
- **Modern JavaScript (ES6+)** - Latest JavaScript features

### Backend
- **Flask** - Lightweight Python web framework
- **scikit-learn** - Machine learning model for predictions
- **pandas & numpy** - Data processing and numerical computing
- **flask-cors** - Enable cross-origin requests from frontend

## Project Structure

```
crop-yield-bot/
│
├── frontend/                    (React Application)
│   ├── src/
│   │   ├── App.jsx             (Main component)
│   │   ├── main.jsx            (Entry point)
│   │   ├── App.css             (Styling)
│   │   ├── index.css           (Global styles)
│   │   └── assets/             (Images, icons)
│   ├── public/                 (Static files)
│   ├── package.json            (Dependencies)
│   ├── vite.config.js          (Build configuration)
│   └── index.html              (HTML entry point)
│
├── backend/                     (Flask API)
│   ├── app.py                  (Main Flask application)
│   ├── requirements.txt        (Python dependencies)
│   ├── model.pkl               (Trained ML model - REQUIRED)
│   └── data/                   (Training datasets)
│
├── SETUP_GUIDE.md              (Detailed setup instructions)
├── setup.bat                   (Windows quick setup)
├── setup.sh                    (macOS/Linux quick setup)
└── README.md                   (Project README)
```

## Quick Start (3 Steps)

### Step 1: Install Dependencies
**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
bash setup.sh
```

**Manual:**
```bash
cd backend && pip install -r requirements.txt && cd ..
cd frontend && npm install && cd ..
```

### Step 2: Start Backend (Terminal 1)
```bash
cd backend
python app.py
```
✓ Runs on: `http://localhost:5000`

### Step 3: Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```
✓ Runs on: `http://localhost:5173`

Open your browser to `http://localhost:5173` 🚀

## API Documentation

### Prediction Endpoint
```
POST /api/predict
Content-Type: application/json

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

Response:
{
  "success": true,
  "yield_ton_per_ha": 4.56,
  "details": { ... }
}
```

### Chatbot Endpoint
```
POST /api/chat
Content-Type: application/json

{
  "message": "What's the best crop for loam soil?"
}

Response:
{
  "success": true,
  "message": "...",
  "reply": "..."
}
```

## Environment Variables

### Backend (.env or .env.local)
```
FLASK_ENV=development
FLASK_DEBUG=True
MODEL_PATH=model.pkl
PORT=5000
```

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:5000
```

## Available Commands

| Command | What it does |
|---------|-------------|
| `npm run dev` | Start dev server with hot reload |
| `npm run build` | Create production build in `dist/` |
| `npm run lint` | Check code quality |
| `npm run preview` | Preview production build |
| `python app.py` | Start Flask backend server |
| `pip install -r requirements.txt` | Install backend dependencies |

## Important Files to Know

1. **frontend/src/App.jsx** - Main React component with UI
2. **backend/app.py** - Flask API with prediction & chat endpoints
3. **backend/model.pkl** - Trained ML model (must exist!)
4. **frontend/package.json** - Frontend dependencies
5. **backend/requirements.txt** - Backend dependencies

## Common Tasks

### Building for Production
```bash
cd frontend
npm run build
# Creates optimized assets in dist/
```

### Testing the API
```bash
# Start backend first: python app.py

# Test prediction endpoint:
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "season": "summer",
    "crop_type": "wheat",
    "soil_type": "loam",
    "temperature": 25,
    "rainfall": 600,
    "humidity": 70,
    "nitrogen": 100,
    "phosphorus": 50,
    "potassium": 40
  }'

# Test chatbot endpoint:
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What crop should I plant?"}'
```

### Debugging
- **Frontend**: Check browser DevTools (F12)
- **Backend**: Flask debug messages appear in terminal
- **Network**: Check browser Network tab to see API calls

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `model.pkl not found` | Ensure trained model exists in backend/ |
| `Port 5000 already in use` | Change port in app.py line 121 |
| `CORS errors` | Backend has CORS enabled, check API URL |
| `npm modules error` | Run `npm install` again |
| `Python dependency error` | Run `pip install -r requirements.txt` |

## Performance Tips

1. **Frontend**: Vite provides instant HMR (hot reload)
2. **Backend**: Flask debug mode auto-restarts on changes
3. **Production**: Run `npm run build` for optimized assets
4. **Caching**: Consider adding Redis for model predictions

## Next Steps

1. ✅ Review this summary
2. ✅ Read SETUP_GUIDE.md for detailed instructions
3. ✅ Run setup script for your OS
4. ✅ Start backend: `python app.py`
5. ✅ Start frontend: `npm run dev`
6. ✅ Open http://localhost:5173
7. ✅ Test predictions and chatbot

## Support Files

- **SETUP_GUIDE.md** - Comprehensive setup and API documentation
- **.env.example** - Environment variable templates
- **setup.bat** - Windows automated setup
- **setup.sh** - macOS/Linux automated setup

---

**Built with ❤️ using React, Flask, and Machine Learning**
