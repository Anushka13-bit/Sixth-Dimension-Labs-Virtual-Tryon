from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.routes import tryon

# Create FastAPI app
app = FastAPI(
    title="Virtual Jewellery Try-On",
    description="Virtual try-on application for jewelry items",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
    os.getenv("FRONTEND_URL", "http://localhost:5173")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving uploaded and generated images
base_dir = Path(__file__).parent.parent.parent
uploads_dir = base_dir / "uploads"
generated_dir = base_dir / "generated"
catalog_dir = base_dir / "catalog"

try:
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")
except Exception as e:
    print(f"Warning: Could not mount uploads directory: {e}")

try:
    app.mount("/generated", StaticFiles(directory=generated_dir), name="generated")
except Exception as e:
    print(f"Warning: Could not mount generated directory: {e}")

try:
    app.mount("/catalog", StaticFiles(directory=catalog_dir), name="catalog")
except Exception as e:
    print(f"Warning: Could not mount catalog directory: {e}")

# Include routes
app.include_router(tryon.router, prefix="/api", tags=["try-on"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Virtual Jewellery Try-On API",
        "version": "1.0.0",
        "endpoints": {
            "catalog": "/api/catalog",
            "try-on": "/api/try-on"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
