# Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Backend Setup (5 minutes)

```bash
# 1. Navigate to backend
cd backend

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Get Google Gemini API Key
# - Visit: https://makersuite.google.com/app/apikey
# - Click "Create API key in new project"
# - Copy the key

# 5. Update .env file
# Replace GEMINI_API_KEY with your actual key
nano .env  # or use your favorite editor

# 6. Start backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend running at `http://localhost:8000`

### Step 2: Frontend Setup (2 minutes)

```bash
# In a new terminal window...

# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start dev server
npm run dev
```

✅ Frontend running at `http://localhost:5173`

## 📝 Testing the Application

1. Open browser to `http://localhost:5173`
2. Upload a face photo (for necklace/earrings)
3. Upload a hand photo (for ring/bracelet)
4. Select a jewelry item from the catalogue
5. Click "Try On"
6. Wait for image generation (takes 30-60 seconds)
7. View and download results!

## ⚙️ Configuration Files

### Backend Configuration
- `.env` - API keys and URLs
- `catalog/catalog.json` - Jewelry items
- `requirements.txt` - Python packages

### Frontend Configuration  
- `.env.local` - API endpoints
- `package.json` - Dependencies
- `vite.config.js` - Build settings

