# 📐 System Architecture

A technical overview of the Smart Labeler embedded vision system using OV7675 + Nano 33 BLE + LLM backend.

---

## 1. Overall Description

This project implements a compact vision system that captures an image, transmits it to a server, processes it with a language model, and displays the keyword result on an OLED screen.

---

## 2. Hardware Components

| Component | Description |
|-----------|-------------|
| OV7675     | 640x480 CMOS image sensor (DVP interface) |
| Nano 33 BLE | ARM Cortex-M4 microcontroller (3.3V) |
| OLED Display (SSD1306) | 128x64 I2C OLED display |
| USB Serial | Communication channel between MCU and server |

---

## 3. Data Flow

```plaintext
1. User triggers capture (button or timed)
2. OV7675 captures frame → Nano reads frame buffer
3. Nano sends image bytes via USB serial to PC/server
4. Server receives image → saves temporarily
5. FastAPI server calls LLM API (e.g., GPT-4o) with image prompt
6. LLM returns a single-word keyword
7. Server sends the keyword back to Nano
8. Nano displays it on OLED
```