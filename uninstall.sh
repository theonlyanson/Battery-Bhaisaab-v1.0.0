#!/usr/bin/env bash

set -Eeuo pipefail

INSTALL_DIR="$HOME/.local/share/battery-bhaisaab"

BIN_DIR="$HOME/.local/bin"

CONFIG_DIR="$HOME/.config/battery-bhaisaab"

SYSTEMD_DIR="$HOME/.config/systemd/user"

SERVICE="battery-monitor.service"

CLI="battery-bhaisaab"

echo
echo "========================================"
echo "🐧 Battery Bhaisaab Uninstaller"
echo "========================================"
echo

echo "[1/7] Stopping service..."

systemctl --user stop "$SERVICE" 2>/dev/null || true

echo "✓ Done"

echo

echo "[2/7] Disabling service..."

systemctl --user disable "$SERVICE" 2>/dev/null || true

echo "✓ Done"

echo

echo "[3/7] Removing service..."

rm -f "$SYSTEMD_DIR/$SERVICE"

systemctl --user daemon-reload

echo "✓ Done"

echo

echo "[4/7] Removing application..."

rm -rf "$INSTALL_DIR"

echo "✓ Done"

echo

echo "[5/7] Removing CLI..."

rm -f "$BIN_DIR/$CLI"

echo "✓ Done"

echo

echo "[6/7] Configuration"

read -rp "Remove configuration too? (y/N): " answer

case "$answer" in

    y|Y)

        rm -rf "$CONFIG_DIR"

        echo "✓ Configuration removed."

        ;;

    *)

        echo "✓ Configuration preserved."

        ;;

esac

echo

echo "[7/7] Finished"

echo

echo "========================================"

echo "Battery Bhaisaab removed successfully."

echo "========================================"

echo
