import threading
import uvicorn
from app.api import app
from interfaces.camera_serial import frame_capture

if __name__ == "__main__":
    threading.Thread(target=frame_capture, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
