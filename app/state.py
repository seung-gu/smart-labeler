from threading import Lock

_latest_image = None
_lock = Lock()

def set_latest_image(img):
    global _latest_image
    with _lock:
        _latest_image = img.copy()

def get_latest_image():
    with _lock:
        return _latest_image.copy() if _latest_image is not None else None
