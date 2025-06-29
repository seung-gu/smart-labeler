# main.py
import serial
import cv2

from llm.gemini_api import query_keywords
from utils.image_utils import decode_rgb565


WIDTH, HEIGHT = 320, 240
FRAME_SIZE = WIDTH * HEIGHT * 2
ser = serial.Serial('/dev/ttyACM0', 230400, timeout=5)

while True:
    print("📡 Requesting RGB frame...")
    ser.write(b"READY\n")

    received = bytearray()
    while len(received) < FRAME_SIZE:
        chunk = ser.read(FRAME_SIZE - len(received))
        if not chunk:
            print(f"⏱️ Timeout. Received only {len(received)} bytes.")
            break
        received.extend(chunk)

    if len(received) != FRAME_SIZE:
        print(f"⚠️ Incomplete frame ({len(received)} bytes), skipping.")
        continue

    img_bgr = decode_rgb565(received, WIDTH, HEIGHT)
    img_zoomed = cv2.resize(img_bgr, (WIDTH * 2, HEIGHT * 2), interpolation=cv2.INTER_NEAREST)
    cv2.imshow("RGB565 Frame", img_zoomed)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        print("🧠 Sending image to Gemini...")
        result = query_keywords(img_bgr)
        print("🔍 Gemini Keywords:", result.strip())

ser.close()
cv2.destroyAllWindows()
