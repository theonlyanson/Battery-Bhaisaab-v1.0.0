#!/usr/bin/env bash

set -Eeuo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

APP_NAME="battery-bhaisaab"
CLI_NAME="battery-bhaisaab"
SERVICE_NAME="battery-monitor.service"

INSTALL_DIR="$HOME/.local/share/$APP_NAME"
BIN_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.config/$APP_NAME"
SYSTEMD_DIR="$HOME/.config/systemd/user"

echo
echo "========================================"
echo "🐧 Battery Bhaisaab Installer"
echo "========================================"
echo

#########################################################
echo "[1/10] Checking Python..."

if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python 3 is not installed."
    exit 1
fi

echo "✓ Python found."
echo

#########################################################
echo "[2/10] Creating directories..."

mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$SYSTEMD_DIR"

echo "✓ Directories ready."
echo

#########################################################
echo "[3/10] Copying application..."

rm -rf "$INSTALL_DIR/src"
rm -rf "$INSTALL_DIR/sounds"

cp -a "$PROJECT_DIR/src" "$INSTALL_DIR/"
cp -a "$PROJECT_DIR/sounds" "$INSTALL_DIR/"

echo "✓ Application copied."
echo

#########################################################
echo "[4/10] Installing CLI..."

install -m 755 "$PROJECT_DIR/$CLI_NAME" "$BIN_DIR/$CLI_NAME"

echo "✓ CLI installed."
echo

#########################################################
echo "[5/10] Preparing configuration..."

# Config.py will automatically create battery.conf
# the first time the application starts.
mkdir -p "$CONFIG_DIR"

echo "✓ Configuration directory ready."
echo

#########################################################
echo "[6/10] Installing systemd service..."

install -m 644 \
    "$PROJECT_DIR/$SERVICE_NAME" \
    "$SYSTEMD_DIR/$SERVICE_NAME"

systemctl --user daemon-reload

echo "✓ Service installed."
echo

#########################################################
echo "[7/10] Enabling service..."

systemctl --user enable "$SERVICE_NAME" >/dev/null 2>&1 || true

echo "✓ Enabled."
echo

#########################################################
echo "[8/10] Restarting service..."

systemctl --user restart "$SERVICE_NAME"

echo "✓ Service running."
echo

#########################################################
echo "[9/10] Running Doctor..."

"$BIN_DIR/$CLI_NAME" doctor || true

echo

#########################################################
echo "[10/10] Finished."

echo
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo

echo "Application:"
echo "  $INSTALL_DIR"

echo
echo "Configuration:"
echo "  $CONFIG_DIR"

echo
echo "Commands:"
echo
echo "battery-bhaisaab status"
echo "battery-bhaisaab doctor"
echo "battery-bhaisaab logs"
echo
