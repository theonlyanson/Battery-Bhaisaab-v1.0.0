#!/usr/bin/env python3

"""
Battery Bhaisaab

Project Paths
"""

from pathlib import Path

HOME = Path.home()

# Installation directory

INSTALL_DIR = HOME / ".local" / "share" / "battery-bhaisaab"

# Source

SRC_DIR = INSTALL_DIR / "src"

# Sounds

SOUND_DIR = INSTALL_DIR / "sounds"

# Logs

LOG_DIR = INSTALL_DIR / "logs"

# Config

CONFIG_DIR = HOME / ".config" / "battery-bhaisaab"

CONFIG_FILE = CONFIG_DIR / "battery.conf"
