#!/usr/bin/env python3
"""
Battery Bhaisaab
----------------

Notification Engine

Responsible only for desktop notifications.

Uses:

notify-send

Nothing else.
"""

from pathlib import Path
import shutil
import subprocess


class NotificationError(Exception):
    pass


class Notify:

    def __init__(self):

        self.command = shutil.which("notify-send")

    def available(self):

        return self.command is not None

    def send(
        self,
        title,
        message,
        urgency="normal",
        icon=None,
        timeout=5000,
    ):

        if not self.available():
            raise NotificationError(
                "notify-send not installed."
            )

        cmd = [
            self.command,
            "-u",
            urgency,
            "-t",
            str(timeout),
        ]

        if icon:

            icon = Path(icon)

            if icon.exists():
                cmd.extend(["-i", str(icon)])

        cmd.extend([title, message])

        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def info(self, title, message):

        self.send(
            title,
            message,
            urgency="normal"
        )

    def warning(self, title, message):

        self.send(
            title,
            message,
            urgency="normal"
        )

    def critical(self, title, message):

        self.send(
            title,
            message,
            urgency="critical",
            timeout=0
        )


if __name__ == "__main__":

    notify = Notify()

    print()

    print("Battery Bhaisaab Notification Engine")

    print("-----------------------------------")

    if notify.available():

        print()

        print("notify-send detected.")

        notify.info(
            "Battery Bhaisaab",
            "Notification test successful."
        )

        print()

        print("Notification sent.")

    else:

        print()

        print("notify-send not installed.")
