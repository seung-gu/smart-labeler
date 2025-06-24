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

### - [#15](https://github.com/seung-gu/smart-labeler/issues/15) Virtual environment setup
This project is configured using `pipenv` for virtual environment and dependency management.

The packages will be managed via `Pipfile` and `Pipfile.lock`.


----
## 2025-06-22
### - [#20](https://github.com/seung-gu/smart-labeler/issues/20) Auto update log development
## 📝 Log Automation Summary

This document explains how automatic logging works for `devlog.md` and `doclog.md` in this project.

---

### 📘 Overview Table

| Feature             | devlog.md                                  | doclog.md                                  |
|---------------------|---------------------------------------------|---------------------------------------------|
| **Trigger**         | Local `git commit` (via pre-push hook)     | GitHub PR merged into `main`               |
| **Data Source**     | Commit message + SHA                        | PR title/body + linked issue               |
| **Update Type**     | Append (by date + issue)                    | Replace full block (per issue)             |
| **Log Scope**       | Developer activity log                      | Documentation summary per feature          |
| **Entry Reference** | Commit → Issue number                       | PR → Issue number (via title)              |
| **Manual Prompts**  | ❌ Disabled                                  | ❌ Disabled                                 |

---

### 🛠 Devlog Rules (docs/devlog.md)

- Triggered on every **local push** (via `.git/hooks/pre-push`)
- Appends commit info under:
  - Date section (e.g. `## 2025-06-21`)
  - Issue section (e.g. `

### - [#15](https://github.com/.../issues/15) Init camera
<PR body and/or issue body>
```

---

### ⚙️ Notes

- `generate_log.py` handles both `devlog` and `doclog` in one entrypoint
- Uses GitHub API with `GH_TOKEN`
- Automatically detects whether it's:
  - Local push → devlog
  - GitHub PR merge → doclog

---

### 🔍 Limitations

- Auto-updated `devlog.md` from the `pre-push` hook is committed during the hook, but **not pushed immediately**. Users must **manually push once more** to sync the devlog update
- Only logs commits that explicitly reference `#<number>`


----
## 2025-06-23
### - [#11](https://github.com/seung-gu/smart-labeler/issues/11) OV7675 camera: wiring, configuration, and signal verification
- [x] Implement a code running OV7675 camera in Nano 33 BLE 
> Nano 33 BLE <----(serial com)----> Desktop 

- [x] Get signal in Desktop through Serial communication
- [x] Verify the signal as an image
- [x] Save RGB image in the desktop when the buffer is full (image is fully received)

> 🧩 Function: `rgb565_to_rgb888(byte1, byte2)`
> 
> 🔧 Purpose
> Converts a **16-bit RGB565** encoded pixel (split across two 8-bit bytes) into an **RGB888** (8 bits per channel) format.
> 
> 🧪 RGB565 Format
> A 16-bit RGB555 pixel is structured as follows:
> 
> > Bit layout:
> > 
> > [15:11] - Red   (5 bits)
> > 
> > [10:5]   - Green (6 bits)
> > 
> > [4:0]   - Blue  (5 bits)
> 
> This format uses **5 - 6 bits per color channel**, aligned to the **most significant bits** to preserve brightness when converting to 8 bits.
>
> 🎯 RGB888 Conversion (8 bits per channel)
> 
> > Red: 5 bits → 8 bits → R << 3
> > 
> > Green: 6 bits → 8 bits → G << 2
> > 
> > Blue: 5 bits → 8 bits → B << 3
> 
> 
> 
> 📎 Notes
> - Many low-power image sensors output RGB565, RGB555, or YUV formats due to bandwidth constraints.
> - **Aligning to MSB(Most Significant Bit) ensures brightness and hue are preserved when rendering on higher-bit displays.**
> - This conversion is **lossy** but visually acceptable for most applications.


----
## 2025-06-24
### - [#12](https://github.com/seung-gu/smart-labeler/issues/12) Button trigger for capturing image
- [x] Button test
> Unfortunately, a switch provided in Tiny machine learning shield does not work  
> https://content.arduino.cc/assets/MachineLearningCarrierV1.0.pdf  
> Official schematic shows that the switch pin connects with Pin 13 (D13) as pull-up resistor  
> But, this Pin 13 shares with LED as the following official pin out  
> https://images.theengineeringprojects.com/image/webp/2021/01/arduino-nano-33-ble.png.webp?ssl=1  
> Therefore, sadly it's not possible to use the switch with a read pin for switch input.  

>  
>  <img src="https://github.com/user-attachments/assets/a2cd54db-cf8c-44af-9acc-66eda51c6bd1" width="300">   
>
>  Another pin was tested (D2) with an external switch, and it worked well.  
> Therefore, the concept (start capturing the image via camera when the button is pressed) will not work if there is no external extra button.  
>  Although, the capturing by switch is failed, but the project will proceed, and the board will be replaced with **Sparkfun Edge** in the near future.  

- [x] Capture an image if the button triggered

