# 🔋 Battery Bhaisaab

> **Your Battery's Best Friend on Linux.**

Battery Bhaisaab is a lightweight battery monitoring daemon for Linux that notifies you when your battery reaches configurable levels, plays custom sounds, alerts you when the charger is connected or disconnected, and lets you know when the battery is fully charged.

Designed for simplicity, reliability, and minimal resource usage.

---

## ✨ Features

- 🔋 Low battery alerts (20%, 15%, 10%, 5% by default)
- 🔌 Charger Connected notification
- 🔌 Charger Removed notification
- 🎉 Battery Full notification
- 🔊 Custom notification sounds
- 🖥 Desktop notifications
- ⚙️ Configurable battery levels
- 🔇 Optional sound notifications
- 📜 Logging support
- 🩺 Built-in diagnostics (`doctor`)
- 🖥 Runs as a systemd user service
- 🚀 Easy installation & removal

---

## 📂 Project Structure

```
battery-bhaisaab/
├── battery-bhaisaab              # CLI
├── install.sh
├── uninstall.sh
├── battery-monitor.service
│
├── sounds/
│   ├── battery20.wav
│   ├── battery15.wav
│   ├── battery10.wav
│   ├── battery5.wav
│   ├── charging.wav
│   ├── discharging.wav
│   └── full.wav
│
└── src/
    ├── audio.py
    ├── battery.py
    ├── config.py
    ├── doctor.py
    ├── logger.py
    ├── monitor.py
    ├── notify.py
    └── paths.py
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/theonlyanson/Battery-Bhaisaab-v1.0.0.git

cd battery-bhaisaab
```

Run the installer

```bash
chmod +x install.sh

./install.sh
```

That's it.

Battery Bhaisaab will automatically install itself and start running as a user service.

---

# Uninstall

```bash
chmod +x uninstall.sh

./uninstall.sh
```

---

# CLI Commands

## Check Status

```bash
battery-bhaisaab status
```

---

## Start Service

```bash
battery-bhaisaab start
```

---

## Stop Service

```bash
battery-bhaisaab stop
```

---

## Restart Service

```bash
battery-bhaisaab restart
```

---

## Run Manually

Useful for debugging.

```bash
battery-bhaisaab run
```

---

## View Logs

```bash
battery-bhaisaab logs
```

---

## Doctor

Runs diagnostics and verifies installation.

```bash
battery-bhaisaab doctor
```

---

## Version

```bash
battery-bhaisaab version
```

---

# Configuration

Configuration file:

```
~/.config/battery-bhaisaab/battery.conf
```

Default configuration:

```ini
[GENERAL]
check_interval = 30
logging = true

[BATTERY]
level1 = 20
level2 = 15
level3 = 10
level4 = 5

[NOTIFICATIONS]
enabled = true
timeout = 5000

low_battery = true
charger_connected = true
charger_removed = true
battery_full = true

[AUDIO]
enabled = true
```

---

# Notification Events

Battery Bhaisaab currently supports:

| Event | Notification | Sound |
|--------|--------------|--------|
|20% Battery|✅|battery20.wav|
|15% Battery|✅|battery15.wav|
|10% Battery|✅|battery10.wav|
|5% Battery|✅|battery5.wav|
|Charger Connected|✅|charging.wav|
|Charger Removed|✅|discharging.wav|
|Battery Full|✅|full.wav|

---

# Logs

Logs are stored in

```
~/.local/share/battery-bhaisaab/logs/
```

You can also watch the service live

```bash
journalctl --user -u battery-monitor.service -f
```

---

# Files Installed

Configuration

```
~/.config/battery-bhaisaab/
```

Logs

```
~/.local/share/battery-bhaisaab/logs/
```

Sounds

```
~/.local/share/battery-bhaisaab/sounds/
```

Executable

```
~/.local/bin/battery-bhaisaab
```

---

# Requirements

- Linux
- Python 3.10+
- systemd
- notify-send
- A supported audio player:
  - paplay
  - pw-play
  - aplay

---

# Tested On

- Kali Linux Rolling
- Python 3.13
- PipeWire
- GNOME
- i3 Window Manager

---

# Troubleshooting

Run

```bash
battery-bhaisaab doctor
```

If the service isn't running

```bash
battery-bhaisaab restart
```

View logs

```bash
battery-bhaisaab logs
```

or

```bash
journalctl --user -u battery-monitor.service -f
```

---

# Version

Current Release

```
v1.0.0
```

---

# Roadmap

Future ideas

- Battery health estimation
- Adaptive notification intervals
- Multiple notification themes
- Custom user sounds
- GUI settings application
- Battery statistics
- Charging history
- Wayland improvements
- Packaging for AUR
- Debian package
- Flatpak support

---

# Contributing

Contributions, suggestions, and bug reports are always welcome.

Feel free to fork the repository and submit a Pull Request.

---

# License

MIT License

---

# Author

**Anson Sarosh Dsouza**

GitHub:
https://github.com/theonlyanson

---

Made with ❤️ and ☕ on Linux.
