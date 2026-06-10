# Virtual Jewellery Try-On

A complete full-stack application for virtual jewelry try-on using AI-generated images and videos. Users upload face/hand photos and virtually try on different jewelry items (rings, bracelets, necklaces, earrings) with photorealistic results powered by the Kling AI model.

## 🌟 Features

- **Upload Photos**: Upload face and hand images for try-on
- **Browse Jewelry**: Browse a curated catalog of jewelry items
- **Virtual Try-On**: Get photorealistic virtual try-on images using PiAPI (Kling Image-to-Image)
- **Video Generation**: Automatically generate cinematic try-on videos using kie.ai (Kling Image-to-Video)
- **Smart Validation**: Automatic validation for jewelry-specific image requirements
- **Download Results**: Download generated images and videos directly to your device
- **Modern UI**: Clean, responsive interface with drag-and-drop upload

## 📋 Project Structure

```
virtual-tryon/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   └── tryon.py           # API endpoints
│   │   ├── services/
│   │   │   ├── piapi_service.py   # PiAPI integration for images
│   │   │   ├── video_service.py   # kie.ai integration for videos
│   │   │   ├── prompt_builder.py  # Dynamic prompt generation
│   │   │   └── catalog_service.py # Catalog management
│   │   ├── models/
│   │   │   └── schemas.py         # Request/response models
│   │   ├── utils/
│   │   │   └── file_handler.py    # File operations
│   │   └── main.py                # FastAPI app
│   ├── catalog/
│   │   └── catalog.json           # Jewelry items catalog
│   ├── uploads/                   # User uploaded images
│   ├── generated/                 # Generated images and videos
│   ├── requirements.txt           # Python dependencies
│   └── .env                       # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageUpload.jsx
│   │   │   ├── CatalogueGrid.jsx
│   │   │   ├── ResultDisplay.jsx
│   │   │   └── *.css              # Component styles
│   │   ├── api/
│   │   │   └── tryon-api.js       # API client
│   │   ├── App.jsx                # Main app component
│   │   ├── App.css                # App styles
│   │   └── main.jsx               # React entry point
│   ├── index.html                 # HTML template
│   ├── package.json               # Node dependencies
│   └── vite.config.js             # Vite configuration
└── README.md                      # This file
```

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern web framework
- **PiAPI** - AI image generation (Kling)
- **kie.ai** - AI video generation (Kling Image-to-Video)
- **Pydantic** - Data validation
- **Python-dotenv** - Environment management
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **CSS3** - Styling with responsive design

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- **PiAPI API Key** (for image generation)
- **kie.ai API Key** (for video generation)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create Python virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   # Copy .env file and update with your values
   cp .env.example .env
   ```
   *Edit `.env` and add your API keys (see APIs section below).*

5. **Run backend server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create .env file**
   ```bash
   echo "VITE_API_URL=http://localhost:8000/api" > .env.local
   ```

4. **Run frontend dev server**
   ```bash
   npm run dev
   ```
   
   Frontend will be available at `http://localhost:5173`

## 🔑 APIs & Setup Guide

This application relies on two external APIs to generate high-quality Kling AI outputs: **PiAPI** (for the try-on images) and **kie.ai** (for animating those images into video).

### 1. PiAPI (Virtual Try-On Images)
Used for the core virtual try-on experience.
1. Create an account at [PiAPI](https://piapi.ai/)
2. Generate an API Key from your dashboard.
3. Top up credits if necessary.
4. Add to your `.env`:
   ```bash
   PIAPI_KEY=your_piapi_key_here
   PIAPI_BASE_URL=https://api.piapi.ai/api/v1/task
   ```

### 2. kie.ai (Cinematic Video Generation)
Used to transform the static try-on image into a smooth, cinematic 5-second video.
1. Create an account at [kie.ai](https://kie.ai/)
2. Generate an API Key from your dashboard.
3. Top up credits if necessary (Error `402` means insufficient credits).
4. Add to your `.env`:
   ```bash
   KIE_API_KEY=your_kie_api_key_here
   KIE_BASE_URL=https://api.kie.ai/v1/videos/image2video
   KIE_AUTH_TYPE=bearer
   ```

## 🔐 Environment Variables (.env)

Your `backend/.env` should look like this:
```
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173

# PiAPI (Image Generation)
PIAPI_KEY=your_key_here
PIAPI_BASE_URL=https://api.piapi.ai/api/v1/task

# kie.ai (Video Generation)
KIE_API_KEY=your_key_here
KIE_BASE_URL=https://api.kie.ai/v1/videos/image2video
KIE_AUTH_TYPE=bearer
```

## 📚 API Endpoints

### GET /api/catalog
Get all jewelry items in the catalog.

### POST /api/try-on
Generate virtual try-on image (Automatically triggers PiAPI).
- **Multipart Form Data**: `jewelry_id`, `face_image` (optional), `hand_image` (optional)

### POST /api/generate-video
Generate video from image (Automatically triggers kie.ai).
- **JSON Body**: `{"image_url": "..."}`

## 🎨 Jewelry Types & Image Requirements

| Type | Required Image | Notes |
|------|---|---|
| Necklace | Face | Placed around neck |
| Earrings | Face | Placed on ears |
| Ring | Hand | Placed on finger |
| Bracelet | Hand | Placed on wrist |

## 🔄 Workflow

1. **Upload Images**: User uploads face and/or hand images
2. **Select Jewelry**: User browses and selects a jewelry item
3. **Try On**: Frontend validates requirements and sends request
4. **Generate Image**: Backend uses PiAPI to generate a photorealistic try-on image
5. **Create Video**: Frontend automatically passes the generated image to `/generate-video` which uses kie.ai to generate a 5-second video.
6. **Display & Download**: User can view and download the image and video results directly from the browser.
