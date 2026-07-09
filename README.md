# HarvestIQ - Documentation Index

## 📚 Documentation Files

Quick navigation to all project documentation:

### 1. **APP_SUMMARY.md** ⭐ START HERE
   - What the application does
   - Quick start (3 steps)
   - Technology stack overview
   - Common tasks
   - API documentation
   - **Best for:** Getting oriented quickly

### 2. **SETUP_GUIDE.md** 🛠️ DETAILED SETUP
   - Complete setup instructions
   - Prerequisite checks
   - Frontend setup (React/Vite)
   - Backend setup (Flask/Python)
   - Running in development
   - Production build
   - Environment configuration
   - Troubleshooting tips
   - **Best for:** Step-by-step setup and configuration

### 3. **DEVELOPMENT_GUIDE.md** 🔧 DEVELOPMENT & DEBUGGING
   - Development workflow
   - Common issues and solutions
   - Advanced debugging techniques
   - Performance optimization
   - Code structure
   - Deployment considerations
   - **Best for:** Troubleshooting and development help

---

## 🚀 Quick Start (Choose Your OS)

### Windows
```bash
setup.bat
```

### macOS / Linux
```bash
bash setup.sh
```

### Manual Setup
```bash
# Backend
cd backend
python -m pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

> Note: The frontend requires Node.js and npm. Install Node.js from https://nodejs.org/ if these tools are not available.
>
> Optional: copy `backend/.env.example` to `backend/.env` and `frontend/.env.example` to `frontend/.env.local` to configure environment variables.

---

## ▶️ Run the Full App

After completing setup, start both services in separate terminals:

```bash
# Terminal 1 - backend
cd backend
python app.py
```

```bash
# Terminal 2 - frontend
cd frontend
npm run dev
```

Then open the app in your browser at:

```bash
http://localhost:5173
```

If the API is hosted elsewhere, set the frontend environment variable before launch:

```bash
cd frontend
set VITE_API_URL=http://localhost:5000
npm run dev
```

---

## �️ Local Troubleshooting Checklist

- Ensure Python 3.8+ is installed and `python --version` works.
- Ensure Node.js and npm are installed and `npm --version` works.
- Run `cd backend && python -m pip install -r requirements.txt`.
- Run `cd frontend && npm install`.
- Start backend first: `cd backend && python app.py`.
- Start frontend next: `cd frontend && npm run dev`.
- Open `http://localhost:5173` in your browser.
- If API calls fail, verify backend is reachable at `http://localhost:5000`.

---

## 📂 Project Files at a Glance
 
| File/Folder | Purpose |
|-------------|---------|
| `setup.bat` | Windows automated setup |
| `setup.sh` | macOS/Linux automated setup |
| `APP_SUMMARY.md` | Quick overview and features |
| `SETUP_GUIDE.md` | Detailed setup instructions |
| `DEVELOPMENT_GUIDE.md` | Troubleshooting and debugging |
| `backend/app.py` | Flask API server |
| `backend/requirements.txt` | Python dependencies |
| `backend/model.pkl` | ML model (REQUIRED) |
| `frontend/src/App.jsx` | React main component |
| `frontend/package.json` | Node dependencies |
| `frontend/.env.example` | Frontend environment variable template |
| `backend/.env.example` | Backend environment variable template |
| `frontend/vite.config.js` | Build configuration |

---

## 🎯 What to Do Next

### First Time Setup?
1. Read **APP_SUMMARY.md** (5 min read)
2. Follow **SETUP_GUIDE.md** (setup section)
3. Run setup script (`setup.bat` or `setup.sh`)
4. Start backend in `backend/`: `python app.py`
5. Start frontend in `frontend/`: `npm run dev`
6. Open `http://localhost:5173`

> Verified: backend APIs are working locally with `python app.py` and Flask test client. Frontend build requires Node.js/npm installed on your machine.

### Running into Issues?
1. Check **DEVELOPMENT_GUIDE.md** (issue solutions)
2. Look for your error in troubleshooting section
3. Follow the recommended solution
4. Run the provided commands

### Ready to Develop?
1. Review code in **APP_SUMMARY.md** (Architecture section)
2. Read **DEVELOPMENT_GUIDE.md** (Development Workflow)
3. Edit files and watch changes auto-reload
4. Use provided debugging tips

### Deploying to Production?
1. Read **DEVELOPMENT_GUIDE.md** (Deployment section)
2. Run `npm run build` for frontend
3. Configure backend for production
4. Deploy to your hosting

---

## 🔍 Finding What You Need

### "How do I set this up?"
→ Read **SETUP_GUIDE.md**

### "What does this app do?"
→ Read **APP_SUMMARY.md**

### "Something's broken, help!"
→ Check **DEVELOPMENT_GUIDE.md** → Troubleshooting section

### "How do I deploy?"
→ Check **DEVELOPMENT_GUIDE.md** → Deployment section

### "How do I write code for this?"
→ Read **DEVELOPMENT_GUIDE.md** → Development Workflow

### "How do I call the API?"
→ Check **SETUP_GUIDE.md** → API Endpoints section

---

## 📊 Technology Overview

```
Frontend Stack:
├── React 19.2.5 (UI Framework)
├── Vite 8.0.10 (Build Tool)
├── JavaScript ES6+ (Language)
└── ESLint (Code Quality)

Backend Stack:
├── Flask (Web Framework)
├── scikit-learn (ML Model)
├── pandas & numpy (Data Processing)
└── Python 3.8+ (Language)

Data:
├── model.pkl (Trained ML Model)
├── Training datasets (in data/)
└── Label encoders (in model.pkl)
```

---

## 🎓 Learning Resources

- **React:** https://react.dev
- **Vite:** https://vite.dev
- **Flask:** https://flask.palletsprojects.com
- **scikit-learn:** https://scikit-learn.org
- **Python:** https://python.org
- **Node.js:** https://nodejs.org

---

## ✅ Checklist Before Starting

- [ ] Node.js v16+ installed
- [ ] Python 3.8+ installed
- [ ] Read APP_SUMMARY.md
- [ ] Ran setup script (or manual setup)
- [ ] Backend can start (`python app.py`)
- [ ] Frontend can start (`npm run dev`)
- [ ] `model.pkl` exists in backend/
- [ ] Port 5000 available for backend
- [ ] Port 5173 available for frontend

---

## 🆘 Emergency Help

**Backend won't start:**
```
1. Check Python is installed: python --version
2. Check dependencies: cd backend && pip install -r requirements.txt
3. Check model.pkl exists: ls backend/model.pkl
4. Check error message in terminal
```

**Frontend won't start:**
```
1. Check Node.js is installed: node --version
2. Check dependencies: cd frontend && npm install
3. Check port 5173 is free
4. Check error message in terminal
```

**API calls failing:**
```
1. Verify backend is running: curl http://localhost:5000/api/chat -X POST
2. Check CORS enabled in backend/app.py
3. Check frontend API URL is correct
4. Check Network tab in browser DevTools
```

---

## 📝 Documentation Version

- **Version:** 1.0
- **Last Updated:** May 2024
- **Maintained By:** Development Team

---

## 🎯 Success Criteria

You'll know everything is working when:

✅ Backend starts without errors  
✅ Frontend loads in browser  
✅ Can see the React UI  
✅ Can make API calls successfully  
✅ Prediction endpoint returns results  
✅ Chatbot endpoint responds  
✅ No CORS or connection errors  
✅ Code changes auto-reload  

---

**Ready to build? Start with APP_SUMMARY.md! 🚀**
