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
  - Issue section (e.g. `### - [#12](...) Add camera interface`)
- Format:

```md
----
## 2025-06-21
### - [#12](https://github.com/.../issues/12) Add camera interface
- 🔧 Commit: Add camera init logic  
  [`abc1234`](https://github.com/.../commit/abc1234)
```

- If commit includes `--ignore-devlog`, it is skipped
- Duplicate SHAs are not added

---

### 📚 Doclog Rules (docs/doclog.md)

- Triggered **only on PR merge to main**
- PR title must include `Merge pull request` and `{issue_number}` in `Merge pull request {issue_of_PR} {user}/{issue_number}-title` (e.g. _Merge pull request #1050 seung-gu/15-blablabla_ )
- Full issue body (not commit) is saved:
  - Replaces any previous log block for that issue
- Format:

```md
----
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

