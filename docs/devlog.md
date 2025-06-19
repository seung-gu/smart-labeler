# 📘 Development Log (Auto-updated from recent push)



## 2025-06-19

- #3 Initialize PlatformIO project for Nano 33 BLE
  ➤ structure
  ➤ 
  ➤ ```
  ➤ smart-labeler/
  ➤ ├── board/                            # Hardware (MCU) source code
  ➤ │   └── nano33ble/                    # Arduino Nano 33 BLE firmware (PlatformIO)
  ➤ │       ├── platformio.ini            # PlatformIO project configuration
  ➤ │       └── src/                      # Firmware source code
  ➤ │           └── main.cpp             # Main application logic (LED, UART, etc.)
  ➤ 
  ➤ ```
  ➤ 
  ➤ 
  ➤ - [x] Initialize PlatformIO project for Nano 33 BLE
  💬 🧩 Problem Summary
  💬 
  💬 When using PlatformIO with platform = nordicnrf52 (latest version), the firmware successfully uploads to the Arduino Nano 33 BLE Sense Lite, but the code does not execute at all (e.g., built-in LED doesn't blink, loop() seems dead).
  💬 
  💬 This does not happen when using Arduino IDE with the same code.
  💬 
  💬 🔍 Cause
  💬 
  💬 The latest nordicnrf52 platform (as of mid-2025) in PlatformIO appears to include an incompatible Arduino core (likely based on Arduino Mbed Core 4.x or similar), which is not properly supported by the Nano 33 BLE.
  💬 
  💬 As a result, the board accepts the binary upload, but the CPU fails to boot the firmware correctly.
  💬 
  💬 ✅ Solution
  💬 
  💬 Pin the platform version explicitly to the last known working release:
  💬 
  💬 `platform = nordicnrf52@9.5.0`
  💬 
  💬 With this version, the firmware executes correctly (e.g., LED blinks, application logic runs) just like in Arduino IDE.
  💬 
  💬 Link :
  💬 https://community.platformio.org/t/blink-sketch-does-not-work-when-uploaded-via-platformio-vscode-ide-but-does-from-arduino-ide-nano-33-ble/33365/5?utm_source=chatgpt.com
  💬 https://github.com/platformio/platform-nordicnrf52/issues/175?utm_source=chatgpt.com

