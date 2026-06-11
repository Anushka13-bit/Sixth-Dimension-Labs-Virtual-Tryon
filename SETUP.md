# Quick Start Guide

## 🚀 Fast Setup

### Step 1: Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install backend dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Keys

Create `backend/.env` and add your keys:

```bash
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173

PIAPI_KEY=your_piapi_key_here
PIAPI_BASE_URL=https://api.piapi.ai/api/v1/task

KIE_API_KEY=your_kie_api_key_here

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
```

#### Get your API keys
- **PiAPI**: Sign up at [https://piapi.ai/](https://piapi.ai/) and generate an API key.
- **kie.ai**: Sign up at [https://kie.ai/](https://kie.ai/) and generate an API key.
- **Cloudinary**: Sign up at [https://cloudinary.com/](https://cloudinary.com/) and retrieve the cloud name, API key, and API secret.

> The backend uploads images to Cloudinary so PiAPI can access them via public URLs.

### Step 3: Start the Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend running at `http://localhost:8000`

### Step 4: Frontend Setup

```bash
# In a new terminal window...
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000/api" > .env.local
npm run dev
```

✅ Frontend running at `http://localhost:5173`

## 📝 Test the App

1. Open `http://localhost:5173`
2. Upload a face image for necklaces/earrings
3. Upload a hand image for rings/bracelets
4. Select a jewelry item
5. Click "Try On"
6. Wait for the generated image and video
7. Download the results

## 🔧 Notes

- The backend uses **PiAPI** to generate the virtual try-on image.
- The backend uses **kie.ai** to convert the image into a short video.
- The backend also uses **Cloudinary** to host uploaded images.
- Keep `backend/.env` private and do not commit it.

