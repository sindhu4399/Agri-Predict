# Development & Troubleshooting Guide

## Setup Checklist

- [ ] Node.js v16+ installed (`node --version`)
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] `model.pkl` file exists in backend folder
- [ ] Backend runs without errors (`python app.py`)
- [ ] Frontend dev server starts (`npm run dev`)
- [ ] No port conflicts (5000 for backend, 5173 for frontend)

## Development Workflow

### Terminal Setup (Recommended)

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
# Expected output:
# WARNING in app.run()... Running on http://127.0.0.1:5000
# (Press CTRL+C to quit)
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Expected output:
# ✔ Rollup watched 1 file and detected change...
# VITE v8.0.10  ready in 350 ms
# ➜  Local:   http://localhost:5173/
# ➜  Press q to quit
```

**Browser:**
```
Open: http://localhost:5173
```

### Making Changes

**Frontend Changes:**
- Edit files in `frontend/src/`
- Changes auto-reload in browser (HMR)
- Check browser console for errors

**Backend Changes:**
- Edit `backend/app.py`
- Flask auto-restarts (debug mode enabled)
- Terminal shows reload messages

## Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'flask'"

**Cause:** Backend dependencies not installed

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

**Or specific module:**
```bash
pip install flask flask-cors joblib pandas numpy scikit-learn
```

---

### Issue 2: "Error: EADDRINUSE: address already in use :::5000"

**Cause:** Another process using port 5000

**Solution Option 1 - Kill the process:**
```bash
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

**Solution Option 2 - Change port:**
Edit `backend/app.py` line 121:
```python
# Change from:
app.run(port=5000, debug=True)
# To:
app.run(port=5001, debug=True)
```

Then update frontend API URL if needed.

---

### Issue 3: "FileNotFoundError: [Errno 2] No such file or directory: 'model.pkl'"

**Cause:** Trained model file missing

**Solution:**
1. Ensure `model.pkl` exists in `backend/` directory
2. Check file path in `backend/app.py` line 11
3. Model file should contain:
   - Trained scikit-learn model
   - Label encoders for season, crop_type, soil_type

**Temporary workaround (for testing):**
Comment out model loading temporarily to test API structure.

---

### Issue 4: "npm ERR! code ERESOLVE"

**Cause:** Dependency conflict

**Solution:**
```bash
cd frontend
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

### Issue 5: CORS Error in Browser Console

**Error:** "Access to XMLHttpRequest blocked by CORS policy"

**Cause:** Frontend trying to call wrong API URL

**Solution:**
1. Check backend is running on `http://localhost:5000`
2. Verify frontend API URL in `App.jsx`:
```javascript
const API_URL = 'http://localhost:5000';
```

3. Backend already has CORS enabled:
```python
CORS(app)  # Allows all origins in development
```

---

### Issue 6: "npm: command not found"

**Cause:** Node.js/npm not installed

**Solution:**
1. Download from: https://nodejs.org/
2. Install LTS version
3. Verify: `node --version` and `npm --version`
4. Restart terminal after install

---

### Issue 7: White screen or blank page

**Cause:** Frontend not connecting to backend, or build issue

**Solution:**
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check Network tab for failed API calls
4. Verify backend is running
5. Check API URL configuration

**Debug:**
```javascript
// Add to App.jsx to test connectivity
fetch('http://localhost:5000/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({message: 'test'})
})
.then(r => r.json())
.then(data => console.log('API works:', data))
.catch(err => console.error('API error:', err))
```

---

## Advanced Debugging

### Backend Debugging

**Enable verbose logging:**
Edit `backend/app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/api/predict", methods=["POST"])
def predict_yield():
    print("Request received:", request.json)  # Debug print
    try:
        # ... code ...
    except Exception as e:
        print(f"Error: {e}")  # Print error
        return jsonify({"success": False, "error": str(e)}), 400
```

**Test API with curl:**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"season":"summer","crop_type":"wheat",...}'
```

---

### Frontend Debugging

**React DevTools:**
1. Install React Developer Tools browser extension
2. Open DevTools (F12)
3. Go to Components tab
4. Inspect component state and props

**Console Logging:**
```javascript
// In App.jsx or components:
console.log('Sending data:', data);
const response = await fetch(API_URL + '/api/predict', {...});
console.log('Response:', response);
```

**Network Inspection:**
1. Open DevTools Network tab
2. Make API call
3. Click request to see:
   - Request headers
   - Request body
   - Response status
   - Response data

---

## Performance Optimization

### Frontend
```bash
# Build for production (optimized)
npm run build

# Preview production build
npm run preview
```

### Backend
For production, disable debug mode:
```python
# Change from:
app.run(port=5000, debug=True)
# To:
app.run(port=5000, debug=False)
```

---

## Database & Data

### Training Data
Located in `backend/data/` (if available)

### Model File
The `model.pkl` file contains:
```python
# Saved with joblib:
import joblib
model, le_crop, le_soil, le_season = joblib.load("model.pkl")
```

### Model Features Expected
```
Input columns:
- season_enc (encoded)
- crop_enc (encoded)
- soil_enc (encoded)
- temperature (float)
- rainfall (float)
- humidity (float)
- nitrogen (float)
- phosphorus (float)
- potassium (float)

Output:
- yield_ton_per_ha (float)
```

---

## Code Structure

### Frontend
```
src/
├── App.jsx         (Main component, API calls)
├── App.css         (Styling)
├── main.jsx        (Entry point)
├── index.css       (Global styles)
└── assets/         (Images, logos)
```

### Backend
```
backend/
├── app.py          (3 sections)
│   ├── Imports
│   ├── Model loading
│   ├── /api/predict endpoint
│   ├── /api/chat endpoint
│   └── Flask run
└── data/           (Training datasets)
```

---

## Git & Version Control

**Useful commands:**
```bash
# Check status
git status

# View changes
git diff

# Add files
git add .

# Commit
git commit -m "Your message"

# Push
git push origin main

# Pull latest
git pull origin main
```

---

## Deployment Considerations

### Frontend Deployment
```bash
npm run build
# Generates dist/ folder
# Deploy contents to static hosting (Vercel, Netlify, etc.)
```

### Backend Deployment
```python
# Production settings in app.py:
app.run(
    host='0.0.0.0',      # Listen on all interfaces
    port=5000,
    debug=False,         # Disable debug mode
    ssl_context='adhoc'  # Add HTTPS if needed
)
```

**Recommended:** Use Gunicorn or Waitress for production:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Useful Resources

- [React Docs](https://react.dev)
- [Vite Docs](https://vite.dev)
- [Flask Docs](https://flask.palletsprojects.com)
- [scikit-learn Docs](https://scikit-learn.org)
- [MDN Web Docs](https://developer.mozilla.org)
- [Stack Overflow](https://stackoverflow.com)

---

## Getting Help

1. Check error messages carefully
2. Review this troubleshooting guide
3. Check browser console (F12)
4. Check terminal output
5. Try the debug commands above
6. Search error message online
7. Review code in App.jsx and app.py

---

**Last Updated:** 2024
**Version:** 1.0
