# 📘 Document Log (Auto-updated from recent push)

----
## 2025-06-19
### - [#3](https://github.com/seung-gu/smart-labeler/issues/3) Initialize PlatformIO project for Nano 33 BLE
structure


```
smart-labeler/
├── board/                            # Hardware (MCU) source code
│   └── nano33ble/                    # Arduino Nano 33 BLE firmware (PlatformIO)
│       ├── platformio.ini            # PlatformIO project configuration
│       └── src/                      # Firmware source code
│           └── main.cpp             # Main application logic (LED, UART, etc.)

```

- [x] Initialize PlatformIO project for Nano 33 BLE
- [x] Code structure updated
- [x] PlatformIO version issue resolved (see in the comment section below)

----
## 2025-06-21
### - [#11](https://github.com/seung-gu/smart-labeler/issues/11) OV7675 camera: wiring, configuration, and signal verification
- [x] Implement a code running OV7675 camera in Nano 33 BLE 
> Nano 33 BLE <----(serial com)----> Desktop 

- [x] Get signal in Desktop through Serial communication
- [x] Verify the signal as an image
- [ ] Save RGB image in the desktop when the buffer is full (image is fully received)

### - [#15](https://github.com/seung-gu/smart-labeler/issues/15) Virtual environment setup
This project is configured using `pipenv` for virtual environment and dependency management.

The packages will be managed via `Pipfile` and `Pipfile.lock`.



----
## 2025-06-22
### - [#20](https://github.com/seung-gu/smart-labeler/issues/20) Auto update log development
Development and documentation log can be automatically updated whenever it's pushed or branch is merged.

In `devlog.md`, every commit message can be updated whenever it's pushed.

In `doclog.md`, every content of tickets can be updated whenever pull request is created and merged.

