from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

from apis.gemini_api import query_keywords
from app.state import get_latest_image
from config.constants import IMAGE_PATH

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/frame")
def get_frame():
    if os.path.exists(IMAGE_PATH):
        return FileResponse(IMAGE_PATH, media_type="image/jpeg")
    return JSONResponse({"error": "Image not available."}, status_code=404)

@app.post("/ask")
def ask():
    img_bgr = get_latest_image()
    if img_bgr is None:
        return JSONResponse({"keywords": None}, status_code=400)
    result = query_keywords(img_bgr)
    return {"keywords": result.strip()}
