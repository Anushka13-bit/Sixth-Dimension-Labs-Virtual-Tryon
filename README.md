# Virtual Jewellery And Apparel Try-On

A complete full-stack application for virtual jewelry try-on using AI-generated images and videos. Users upload face/hand photos and virtually try on different jewelry items (rings, bracelets, necklaces, earrings) with photorealistic results powered by Kling AI models.

## 🌟 Features

- **Upload Photos**: Upload face and hand images for try-on
- **Browse Jewelry**: Browse a curated catalog of jewelry items
- **Virtual Try-On**: Generate photorealistic try-on images with PiAPI
- **Video Generation**: Create cinematic try-on videos with kie.ai
- **Smart Validation**: Enforce jewelry-specific image requirements
- **Download Results**: Download generated images and videos
- **Modern UI**: Clean, responsive React interface

## 📋 Project Structure

```
virtual-tryon/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   └── tryon.py           # API endpoints
│   │   ├── services/
│   │   │   ├── piapi_service.py   # PiAPI integration for image try-on
│   │   │   ├── video_service.py   # kie.ai integration for video generation
│   │   │   ├── prompt_builder.py  # Natural-language prompt builder
│   │   │   └── catalog_service.py # Jewelry catalog loader
│   │   ├── models/
│   │   │   └── schemas.py         # Request/response models
│   │   ├── utils/
│   │   │   └── file_handler.py    # File upload/download helpers
│   │   └── main.py                # FastAPI app entrypoint
│   ├── catalog/
│   │   └── catalog.json           # Jewelry items metadata
│   ├── uploads/                   # User uploaded images
│   ├── generated/                 # Generated images and videos
│   └── requirements.txt           # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageUpload.jsx
│   │   │   ├── CatalogueGrid.jsx
│   │   │   ├── ResultDisplay.jsx
│   │   │   └── *.css              # Component styles
│   │   ├── api/
│   │   │   └── tryon-api.js       # Frontend API client
│   │   ├── App.jsx                # Main app component
│   │   ├── App.css                # App styles
│   │   └── main.jsx               # React entrypoint
│   ├── index.html                 # HTML template
│   ├── package.json               # Node dependencies
│   └── vite.config.js             # Vite configuration
└── README.md                      # Project documentation
```

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Web API framework
- **PiAPI** - AI image generation service
- **kie.ai** - AI video generation service
- **Cloudinary** - Image hosting for public URLs
- **Pydantic** - Data validation
- **Python-dotenv** - Environment configuration
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **CSS3** - Styling and layout

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- **PiAPI API Key**
- **kie.ai API Key**
- **Cloudinary account and API credentials**

### Backend Setup

1. **Navigate to backend**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create your environment file**
   ```bash
   nano .env
   ```
   Add the required keys listed below.

5. **Run the backend**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure the frontend API URL**
   ```bash
   echo "VITE_API_URL=http://localhost:8000/api" > .env.local
   ```

4. **Start the frontend**
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:5173`

## 🔑 APIs Used and How to Get Them

This project uses the following external services:

- **PiAPI** for image-based virtual try-on
- **kie.ai** for converting generated images into videos
- **Cloudinary** for hosting uploaded images as public URLs

### PiAPI
1. Go to [https://piapi.ai/](https://piapi.ai/)
2. Sign up and verify your account
3. Create an API key from the dashboard
4. Add it to `backend/.env`:
   ```bash
   PIAPI_KEY=your_piapi_key_here
   PIAPI_BASE_URL=https://api.piapi.ai/api/v1/task
   ```

### kie.ai
1. Go to [https://kie.ai/](https://kie.ai/)
2. Sign up and verify your account
3. Create an API key from the dashboard
4. Add it to `backend/.env`:
   ```bash
   KIE_API_KEY=your_kie_api_key_here
   ```

### Cloudinary
1. Go to [https://cloudinary.com/](https://cloudinary.com/)
2. Sign up for a free account
3. Get your Cloud name, API key, and API secret
4. Add them to `backend/.env`:
   ```bash
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_cloudinary_api_key
   CLOUDINARY_API_SECRET=your_cloudinary_api_secret
   ```

## 🔐 Backend Environment Variables

Create `backend/.env` with the following values:

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

> Keep `backend/.env` secret and do not commit it to Git.

## 📚 API Endpoints

### GET /api/catalog
Returns available jewelry items.

### POST /api/try-on
Starts virtual try-on image generation.
- **Form fields**: `jewelry_id`, `face_image` (optional), `hand_image` (optional)

### GET /api/try-on/{task_id}
Returns status and generated image URL for a PiAPI task.

### POST /api/generate-video
Starts kie.ai video generation from a generated image URL.
- **JSON body**: `{ "image_url": "..." }`

## 🎨 Jewelry Types & Image Requirements

| Jewelry Type | Required Upload | Notes |
|--------------|-----------------|-------|
| Necklace | Face image | Upload a portrait image with neck visible |
| Earrings | Face image | Upload a portrait image with ears visible |
| Ring | Hand image | Upload a hand image with fingers visible |
| Bracelet | Hand image | Upload a hand image with wrist visible |

## 🔄 User Flow

1. Upload a face or hand photo.
2. Select a jewelry item.
3. Send the try-on request to the backend.
4. Backend uploads images to Cloudinary and calls PiAPI.
5. Frontend polls for the image generation result.
6. Frontend sends the generated image URL to `/api/generate-video`.
7. Backend calls kie.ai to create a 5-second video.
8. User views and downloads the generated image and video.

SCREENSHOTS-

<img width="1470" height="956" alt="image" src="https://github.com/user-attachments/assets/ae4b1ef7-b998-4ad7-8d2d-6c9e7556af0d" />

uploaded face image-
<img width="4032" height="3024" alt="IMG_8057" src="https://github.com/user-attachments/assets/dfb1357d-3ce6-466b-b25e-f92aeea64694" />

jewelery chosen- 
<img width="194" height="259" alt="image" src="https://github.com/user-attachments/assets/8e6e2c4c-9c71-48ed-9e7f-a98d1d3b1cd2" />

image generated-
<img width="1094" height="1294" alt="image" src="https://github.com/user-attachments/assets/bb69ec4e-2c4d-44cb-bcc5-099383f4a8c7" />

VIDEO DEMONSTRATION-
https://drive.google.com/file/d/1ACYAOSSRMF_z3SyJTzKJOYRL5nJvmI0R/view?usp=sharing

APPAREL TRYON-
model-image:
<img width="198" height="255" alt="model" src="https://github.com/user-attachments/assets/6ee14324-e03c-45a9-980a-915cf7a41c0a" />

Top try-on result: 
<img width="515" height="693" alt="image" src="https://github.com/user-attachments/assets/31dd8cb6-e88c-482a-9784-515be5fa085f" />










