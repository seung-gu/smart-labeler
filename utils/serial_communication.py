import serial
import numpy as np
import cv2

ser = serial.Serial('/dev/ttyACM0', 230400, timeout=5)

WIDTH, HEIGHT = 320, 240
FRAME_SIZE = WIDTH * HEIGHT * 2  # 2 bytes per pixel for RGB565

def decode_rgb565(data):
    """
    Convert RGB565 (R: 5bits, G: 6bits, B: 5bits) raw bytes into RGB888 image.
    byte1: RRRRRGGG
    byte2: GGGBBBBB
    r : 5 upper bits of byte1 (RRRRRXXX)
    g : 3 lower bits of byte1 (XXXXXGGG) + 3 upper bits of byte2 (GGGXXXXX)
    b : 5 lower bits of byte2 (XXXBBBBB)
    in RGB888 format, bits should be upper
    """
    data = np.frombuffer(data, dtype=np.uint8)
    byte1 = data[0::2]  # even indices
    byte2 = data[1::2]  # odd indices

    r = (byte1 & 0b11111000)
    g = ((byte1 & 0b00000111) << 5) | ((byte2 & 0b11100000) >> 3)
    b = (byte2 & 0b00011111) << 3

    bgr = np.stack((b, g, r), axis=-1).reshape((HEIGHT, WIDTH, 3))
    return bgr

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

    img_bgr = decode_rgb565(received)  # opencv expects BGR format
    img_zoomed = cv2.resize(img_bgr, (WIDTH * 2, HEIGHT * 2), interpolation=cv2.INTER_NEAREST)

    cv2.imshow("RGB565 Frame", img_zoomed)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ser.close()
cv2.destroyAllWindows()