/*
  OV767X - Camera Capture Raw Bytes

  This sketch reads a frame from the OmniVision OV7670 camera
  and writes the bytes to the Serial port. Use the Procesing
  sketch in the extras folder to visualize the camera output.

  Circuit:
    - Arduino Nano 33 BLE board
    - OV7670 camera module:
      - 3.3 connected to 3.3
      - GND connected GND
      - SIOC connected to A5
      - SIOD connected to A4
      - VSYNC connected to 8
      - HREF connected to A1
      - PCLK connected to A0
      - XCLK connected to 9
      - D7 connected to 4
      - D6 connected to 6
      - D5 connected to 5
      - D4 connected to 3
      - D3 connected to 2
      - D2 connected to 0 / RX
      - D1 connected to 1 / TX
      - D0 connected to 10

  This example code is in the public domain.
*/

#include <Arduino_OV767X.h>

int bytesPerFrame;
byte data[320 * 240 * 2];

void setup() {
  Serial.begin(230400);
  while (!Serial);

  if (!Camera.begin(QVGA, RGB565, 1)) {
    Serial.println("Failed to initialize camera!");
    while (1);
  }
  bytesPerFrame = Camera.width() * Camera.height() * Camera.bytesPerPixel();  // == 2
}

void loop() {
  // 1. Wait for signal from host
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    if (cmd == "READY") {
      Camera.readFrame(data);
      Serial.write(data, bytesPerFrame);  // send entire RGB565 frame
    }
  }
}
