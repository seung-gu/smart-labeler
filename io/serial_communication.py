import serial
import cv2
from utils.image_utils import decode_rgb565


ser = serial.Serial('/dev/ttyACM0', 230400, timeout=5)

WIDTH, HEIGHT = 320, 240
FRAME_SIZE = WIDTH * HEIGHT * 2  # 2 bytes per pixel for RGB565


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

    img_bgr = decode_rgb565(received, WIDTH, HEIGHT)  # opencv expects BGR format
    img_zoomed = cv2.resize(img_bgr, (WIDTH * 2, HEIGHT * 2), interpolation=cv2.INTER_NEAREST)

    cv2.imshow("RGB565 Frame", img_zoomed)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ser.close()
cv2.destroyAllWindows()