#!/usr/bin/env python3

"""
Battery Bhaisaab

Doctor Module
"""

import shutil
import subprocess
import sys

from audio import Audio
from battery import Battery
from config import Config
from notify import Notify
from paths import CONFIG_FILE, LOG_DIR, SOUND_DIR


class Doctor:

    def __init__(self):

        self.results = []

    # ---------------------------------------------------------

    def add(self, title, status, info=""):

        self.results.append((title, status, info))

    # ---------------------------------------------------------

    def check_python(self):

        version = ".".join(
            map(str, sys.version_info[:3])
        )

        self.add("Python", True, version)

    # ---------------------------------------------------------

    def check_battery(self):

        battery = Battery()

        info = battery.info()

        self.add("Battery", True, info.name)

        self.add(
            "Manufacturer",
            True,
            info.manufacturer
        )

        self.add(
            "Status",
            True,
            info.status
        )

        self.add(
            "Charge",
            True,
            f"{info.capacity}%"
        )

    # ---------------------------------------------------------

    def check_audio(self):

        audio = Audio()

        if audio.player:

            self.add(
                "Audio Backend",
                True,
                audio.player
            )

        else:

            self.add(
                "Audio Backend",
                False,
                "None"
            )

    # ---------------------------------------------------------

    def check_notify(self):

        notify = Notify()

        if notify.available():

            self.add(
                "Notifications",
                True,
                "notify-send"
            )

        else:

            self.add(
                "Notifications",
                False,
                "Missing"
            )

    # ---------------------------------------------------------

    def check_config(self):

        Config()

        if CONFIG_FILE.exists():

            self.add(
                "Configuration",
                True,
                str(CONFIG_FILE)
            )

        else:

            self.add(
                "Configuration",
                False,
                "Missing"
            )

    # ---------------------------------------------------------

    def check_logs(self):

        if LOG_DIR.exists():

            self.add(
                "Logs",
                True,
                str(LOG_DIR)
            )

        else:

            self.add(
                "Logs",
                False,
                "Missing"
            )

    # ---------------------------------------------------------

    def check_sounds(self):

        required = [

            "battery20.wav",

            "battery15.wav",

            "battery10.wav",

            "battery5.wav"

        ]

        missing = []

        for sound in required:

            if not (SOUND_DIR / sound).exists():

                missing.append(sound)

        if missing:

            self.add(

                "Sounds",

                False,

                ", ".join(missing)

            )

        else:

            self.add(

                "Sounds",

                True,

                "All Present"

            )

    # ---------------------------------------------------------

    def check_systemd(self):

        if shutil.which("systemctl"):

            self.add(

                "systemd",

                True,

                "Available"

            )

        else:

            self.add(

                "systemd",

                False,

                "Missing"

            )

    # ---------------------------------------------------------

    def check_service(self):

        result = subprocess.run(

            [

                "systemctl",

                "--user",

                "is-active",

                "battery-monitor.service"

            ],

            capture_output=True,

            text=True

        )

        status = result.stdout.strip()

        if status == "active":

            self.add(

                "Service",

                True,

                "Running"

            )

        else:

            self.add(

                "Service",

                False,

                status

            )

    # ---------------------------------------------------------

    def run(self):

        self.check_python()

        self.check_battery()

        self.check_audio()

        self.check_notify()

        self.check_config()

        self.check_logs()

        self.check_sounds()

        self.check_systemd()

        self.check_service()

        print()

        print("=" * 60)

        print("🐧 Battery Bhaisaab Doctor")

        print("=" * 60)

        print()

        healthy = True

        for title, ok, info in self.results:

            icon = "✔" if ok else "✘"

            if not ok:

                healthy = False

            print(f"{icon} {title:<18} {info}")

        print()

        print("=" * 60)

        if healthy:

            print("Overall Health : 🟢 Excellent")

        else:

            print("Overall Health : 🟡 Needs Attention")

        print("=" * 60)

        print()


if __name__ == "__main__":

    Doctor().run()
