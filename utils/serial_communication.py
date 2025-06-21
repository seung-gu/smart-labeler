import serial
import numpy as np
import cv2

# serial port open
ser = serial.Serial('/dev/ttyACM0', 230400, timeout=5)

# Image size (should be the same size from the board)
WIDTH, HEIGHT = 320, 240
FRAME_SIZE = WIDTH * HEIGHT  # 1 byte per pixel (binary image)


while True:
    print("Waiting for frame...")
    received = bytearray()

    while len(received) < FRAME_SIZE:
        chunk = ser.read(FRAME_SIZE - len(received))
        if not chunk:
            print(f"Timed out. Only received {len(received)} bytes.")
            break
        received.extend(chunk)

    if len(received) != FRAME_SIZE:
        print(f"Incomplete frame ({len(received)} bytes), skipping.")
        continue

    # Frame ready
    img = np.frombuffer(received, dtype=np.uint8).reshape((HEIGHT, WIDTH))
    img_zoomed = cv2.resize(img * 255, (WIDTH * 2, HEIGHT * 2), interpolation=cv2.INTER_NEAREST)

    cv2.imshow("Binary Frame", img_zoomed)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ser.close()
cv2.destroyAllWindows()
