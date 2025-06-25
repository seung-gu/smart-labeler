# Smart Labeler

A lightweight embedded AI system that captures an image using the OV7675 camera, sends it to a cloud-based LLM server, and displays the identified keyword on an OLED screen.

---

## 🧠 Overview

**Smart Labeler** is an end-to-end embedded vision project combining microcontroller-based image capture with cloud AI inference.  
It uses:

- 📷 OV7675 camera module
- 🧠 Arduino Nano 33 BLE (via PlatformIO)
- 🔌 USB Serial connection
- 🌐 FastAPI + OpenAI or Gemini LLM backend
- 🖥 OLED display for keyword output

---

## 🎯 Project Goals

- ✅ Capture images with the OV7675 camera
- ✅ Send the image to a FastAPI server over USB serial
- ✅ Analyze the image using a cloud-based LLM
- ✅ Extract and return a single keyword description
- ✅ Display the result on a small OLED screen

---

## ⚙️ System Architecture

```plaintext
[OV7675 Camera]
       ↓
[Nano 33 BLE (PlatformIO)]
       ↓ USB Serial
[FastAPI Server + LLM (e.g. GPT-4o)]
       ↓
{"keyword": "banana"}
       ↓
[OLED Display]

🧪 Project Structure

smart-labeler/
├── nano/                  # Arduino firmware (PlatformIO)
│   ├── platformio.ini
│   └── src/
│       └── main.cpp
│
├── server/                # FastAPI server with LLM integration
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docs/                  # System architecture, prompt design, experiment logs
│   └── architecture.md
│
├── images/                # Sample captured images
│   └── sample.jpg
│
├── scripts/               # Utility tools (e.g., USB serial receiver)
│   └── serial_receiver.py
│
├── README.md              # This file
└── LICENSE
```
----
## 🚀 Getting Started


### 1. Upload firmware to Nano 33 BLE

    cd nano/
    platformio run --target upload
    platformio device monitor

Ensure the OV7675 is properly connected and configured in main.cpp.

----
### 2. Start FastAPI server (LLM backend)

    cd server/
    docker build -t smart-labeler-server .
    docker run -p 8000:8000 smart-labeler-server

Server will accept image via POST, call the LLM, and return a JSON like:

    { "keyword": "banana" }
----
### 3. Receive image from Nano and forward to server

    cd scripts/
    python serial_receiver.py

This script:

    Reads raw image from USB serial

    Saves it to disk

    Sends it to FastAPI server via HTTP POST

    Prints keyword response

----
## 📄 Documentation

See [docs/doclog.md](docs/doclog.md) for system design, data flow, and prompt engineering notes.


----
## 📘 Development Log

See [docs/devlog.md](docs/devlog.md) for development log.

----
## 📅 Development Roadmap 

You can follow the project development at

👉 [GitHub Projects Roadmap](https://github.com/users/seung-gu/projects/5)
