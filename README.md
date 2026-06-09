# Virtual Jewellery Try-On

A complete full-stack application for virtual jewelry try-on using AI-generated images. Users upload face/hand photos and virtually try on different jewelry items (rings, bracelets, necklaces, earrings) with photorealistic results.

## 🌟 Features

- **Upload Photos**: Upload face and hand images for try-on
- **Browse Jewelry**: Browse a curated catalog of jewelry items
- **Virtual Try-On**: Get photorealistic virtual try-on images using Google Gemini AI
- **Video Generation**: Generated try-on videos for product showcase
- **Smart Validation**: Automatic validation for jewelry-specific image requirements
- **Download Results**: Download generated images and videos
- **Modern UI**: Clean, responsive interface with drag-and-drop upload

## 📋 Project Structure

```
virtual-tryon/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   └── tryon.py           # API endpoints
│   │   ├── services/
│   │   │   ├── gemini_service.py  # Gemini API integration
│   │   │   ├── video_service.py   # Video generation
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
- **Google Generative AI** - AI image generation
- **Pillow** - Image processing
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
- Google Gemini API key

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
   cp .env .env.local
   # Edit .env.local and add your Google Gemini API key
   ```

5. **Create placeholder jewelry images** (optional, for catalog display)
   ```bash
   mkdir -p catalog
   # Add your jewelry images as .jpg files to the catalog directory
   ```

6. **Run backend server**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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
   # Create .env.local file
   echo "VITE_API_URL=http://localhost:8000/api" > .env.local
   ```

4. **Run frontend dev server**
   ```bash
   npm run dev
   ```
   
   Frontend will be available at `http://localhost:5173`

## 🔑 Free APIs & Setup Guide

### Google Gemini API (Required)

This application uses **Google Generative AI (Gemini)** for photorealistic virtual try-on image generation.

**Why Gemini API?**
- ✅ **Completely FREE** - No credit card required for initial use
- ✅ **High Quality** - State-of-the-art AI image generation
- ✅ **Easy Setup** - Simple REST API with Python SDK
- ✅ **Generous Free Tier** - 60 requests/minute, no daily hard limit

**Getting Your API Key (2 minutes):**

1. Visit: [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **"Create API key in new project"**
3. **Copy** the generated API key
4. Add to `backend/.env`:
   ```bash
   GEMINI_API_KEY=your_copied_key_here
   ```

**Verify It Works:**
```bash
# After setup, test the API
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

### Free Tier Rate Limits & Workarounds

**Default Limits:**
- **Rate**: 60 requests per minute
- **Daily**: No hard limit (fair use)
- **Cost**: Always FREE for development

**If You Hit Rate Limit (429 Error):**

1. **Automatic Handling** (Built-in):
   - Frontend shows: "Rate limited - please wait"
   - Suggested wait: 60 seconds

2. **Manual Workaround**:
   ```bash
   # Space out requests with delays
   # Best practice: 5-10 seconds between requests during testing
   # Avoid rapid successive clicks on "Try On" button
   ```

3. **Testing Tips**:
   - Use same image for multiple tries (to test quickly)
   - Wait between different requests
   - Test during off-peak hours for better availability

4. **For Production Use**:
   - Monitor your usage in Google AI Studio
   - Paid tier available if needed: [Google AI Pricing](https://ai.google.dev/pricing)
   - Generous free tier covers most use cases

### Other Services (No API Keys Needed)

- **Pillow** - Image processing (local library)
- **Uvicorn** - Web server (local library)
- **Vite** - Frontend dev tool (local library)
- **FastAPI** - Backend framework (local library)

All other dependencies are local and don't require external API keys.

## 🔐 Environment Variables

### Backend (.env)
```
GEMINI_API_KEY=your_google_gemini_api_key_here
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:8000/api
```

## 📚 API Endpoints

### GET /api/catalog
Get all jewelry items in the catalog.

**Response:**
```json
[
  {
    "id": "1",
    "name": "Gold Necklace",
    "type": "necklace",
    "image": "necklace1.jpg",
    "description": "Elegant gold necklace"
  }
]
```

### POST /api/try-on
Generate virtual try-on image.

**Request:**
```
multipart/form-data:
- jewelry_id (string): ID of jewelry from catalog
- face_image (file, optional): User's face photo
- hand_image (file, optional): User's hand photo
```

**Validation:**
- For `ring` or `bracelet`: `hand_image` is required
- For `necklace` or `earrings`: `face_image` is required

**Response:**
```json
{
  "image_url": "http://localhost:8000/generated/generated_abc123.jpg",
  "video_url": "http://localhost:8000/generated/video_abc123.mp4",
  "message": "Try-on image generated successfully"
}
```

**Error Response:**
```json
{
  "error": "Bad Request",
  "detail": "Hand image required for ring try-on"
}
```

## 🎨 Jewelry Types & Image Requirements

| Type | Required Image | Notes |
|------|---|---|
| Necklace | Face | Placed around neck |
| Earrings | Face | Placed on ears |
| Ring | Hand | Placed on finger |
| Bracelet | Hand | Placed on wrist |

## 💾 Catalog Format

The catalog is defined in `backend/catalog/catalog.json`:

```json
[
  {
    "id": "1",
    "name": "Gold Necklace",
    "type": "necklace",
    "image": "necklace1.jpg",
    "description": "Elegant gold necklace with premium finish"
  }
]
```

Add more items by extending this JSON array.

## 🔄 Workflow

1. **Upload Images**: User uploads face and/or hand images
2. **Select Jewelry**: User browses and selects a jewelry item
3. **Try On**: Frontend validates requirements and sends request
4. **Generate**: Backend uses Gemini API to generate try-on image
5. **Create Video**: Video is generated from the try-on image
6. **Display Results**: Generated image and video are displayed
7. **Download**: User can download results

## 📸 Screenshots & Demo

### Application Flow

**Step 1: Upload Images**
- Drag and drop face photo (for necklace/earrings)
- Drag and drop hand photo (for ring/bracelet)
- Clear visual feedback showing successful uploads

**Step 2: Browse Jewelry**
- Grid display of 6+ jewelry items
- Each item shows: image, name, type, description
- Click to select item (highlighted with checkmark)

**Step 3: Click "Try On"**
- Validates image requirements based on jewelry type
- Shows loading spinner during processing (30-60 seconds)
- Displays error message if validation fails

**Step 4: View Results**
- High-quality generated image
- Embedded video player
- Download buttons for both image and video

