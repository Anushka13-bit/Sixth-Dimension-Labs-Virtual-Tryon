from dotenv import load_dotenv
load_dotenv()   # MUST BE FIRST

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routes.tryon import router as tryon_router


app = FastAPI(
    title="Virtual Jewellery Try-On",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static folders
base_dir = Path(__file__).parent.parent
uploads = base_dir / "uploads"
generated = base_dir / "generated"
catalog = base_dir / "catalog"

app.mount("/uploads", StaticFiles(directory=uploads), name="uploads")
app.mount("/generated", StaticFiles(directory=generated), name="generated")
app.mount("/catalog", StaticFiles(directory=catalog), name="catalog")

# Routes
app.include_router(tryon_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Jewellery Try-On API Running"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
