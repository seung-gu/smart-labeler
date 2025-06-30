import serial
import cv2
from utils.image_utils import decode_rgb565
from app.state import set_latest_image
from config.constants import WIDTH, HEIGHT, IMAGE_PATH, SERIAL_PORT, SERIAL_BAUDRATE, SERIAL_TIMEOUT


FRAME_SIZE = WIDTH * HEIGHT * 2
ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT)

def frame_capture():
    while True:
        ser.write(b"READY\n")
        received = bytearray()
        while len(received) < FRAME_SIZE:
            chunk = ser.read(FRAME_SIZE - len(received))
            if not chunk:
                break
            received.extend(chunk)
        if len(received) != FRAME_SIZE:
            continue

        img_bgr = decode_rgb565(received, WIDTH, HEIGHT)
        set_latest_image(img_bgr)
        cv2.imwrite(IMAGE_PATH, img_bgr)

    ser.close()
    cv2.destroyAllWindows()
