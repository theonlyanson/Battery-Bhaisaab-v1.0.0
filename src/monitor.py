#!/usr/bin/env python3

"""
Battery Bhaisaab

Battery Monitoring Daemon
"""

import signal
import sys
import time

from audio import Audio, AudioError
from battery import Battery
from config import Config
from logger import Logger
from notify import Notify
from paths import SOUND_DIR


class BatteryMonitor:

    def __init__(self):

        self.cfg = Config()

        self.battery = Battery()

        self.audio = Audio()

        self.notify = Notify()

        self.log = Logger()

        # Battery levels already warned
        self.warned = set()

        # Previous battery state
        self.previous_status = None
        self.previous_capacity = None

        # Prevent repeated full battery alerts
        self.full_notified = False

        signal.signal(
            signal.SIGINT,
            self.shutdown
        )

        signal.signal(
            signal.SIGTERM,
            self.shutdown
        )

    # -----------------------------------------------------

    def shutdown(self, *_):

        self.log.info(
            "Battery Bhaisaab stopped."
        )

        print()

        print(
            "Battery Bhaisaab shutting down..."
        )

        sys.exit(0)

    # -----------------------------------------------------

    def play_sound(self, filename):

        try:

            sound = SOUND_DIR / filename

            self.audio.play(sound)

        except AudioError as e:

            self.log.error(str(e))

        except Exception as e:

            self.log.error(str(e))

    # -----------------------------------------------------

    def notify_user(
        self,
        title,
        message,
        critical=False
    ):

        if not self.cfg.notifications:

            return

        try:

            if critical:

                self.notify.critical(
                    title,
                    message
                )

            else:

                self.notify.warning(
                    title,
                    message
                )

        except Exception as e:

            self.log.error(str(e))

    # -----------------------------------------------------

    def log_event(
        self,
        message,
        warning=False
    ):

        if warning:

            self.log.warning(message)

        else:

            self.log.info(message)

    # -----------------------------------------------------

    def handle_charger_connected(
        self,
        info
    ):

        if (
            self.previous_status == "Discharging"
            and info.status == "Charging"
        ):

            if self.cfg.charger_connected_notifications:

                self.notify_user(

                    "🔌 Charger Connected",

                    (
                        f"Charging started.\n"
                        f"Battery : {info.capacity}%"
                    )

                )

            if self.cfg.audio:

                self.play_sound(
                    "charging.wav"
                )

            self.log_event(
                f"Charger connected ({info.capacity}%)."
            )

    # -----------------------------------------------------

    def handle_charger_removed(
        self,
        info
    ):

        if (
            self.previous_status == "Charging"
            and info.status == "Discharging"
        ):

            if self.cfg.charger_removed_notifications:

                self.notify_user(

                    "🔋 Charger Removed",

                    (
                        f"Running on battery.\n"
                        f"Battery : {info.capacity}%"
                    )

                )

            if self.cfg.audio:

                self.play_sound(
                    "discharging.wav"
                )

            self.warned.clear()

            self.full_notified = False

            self.log_event(
                f"Charger removed ({info.capacity}%)."
            )

    # -----------------------------------------------------

    def handle_full_battery(
        self,
        info
    ):

        if (
            info.status == "Charging"
            and info.capacity >= 100
            and not self.full_notified
        ):

            if self.cfg.battery_full_notifications:

                self.notify_user(

                    "🔋 Battery Full",

                    "Battery is fully charged.",

                    critical=False

                )

            if self.cfg.audio:

                self.play_sound(
                    "full.wav"
                )

            self.log_event(
                "Battery fully charged."
            )

            self.full_notified = True

        if info.status != "Charging":

            self.full_notified = False

        elif info.capacity < 100:

            self.full_notified = False

    # -----------------------------------------------------

    def handle_low_battery(
        self,
        info
    ):

        if info.status != "Discharging":

            self.warned.clear()

            return

        if not self.cfg.low_battery_notifications:

            return

        levels = [

            self.cfg.level1,

            self.cfg.level2,

            self.cfg.level3,

            self.cfg.level4,

        ]

        for level in levels:

            if (

                info.capacity <= level

                and level not in self.warned

            ):

                title = "🐧 Battery Bhaisaab"

                message = (

                    f"Battery reached {level}%\n"

                    f"Current Battery : {info.capacity}%\n"

                    f"Status : {info.status}"

                )

                self.notify_user(

                    title,

                    message,

                    critical=(level <= self.cfg.level4)

                )

                if self.cfg.audio:

                    self.play_sound(

                        f"battery{level}.wav"

                    )

                self.log_event(

                    f"Battery reached {level}%",

                    warning=True

                )

                self.warned.add(level)

    # -----------------------------------------------------

    def check(self):

        try:

            info = self.battery.info()

        except Exception as e:

            self.log.error(

                f"Battery read failed: {e}"

            )

            return

        self.handle_charger_connected(

            info

        )

        self.handle_charger_removed(

            info

        )

        self.handle_full_battery(

            info

        )

        self.handle_low_battery(

            info

        )

        self.previous_status = info.status

        self.previous_capacity = info.capacity

    # -----------------------------------------------------

    def run(self):

        self.log.info(

            "Battery Bhaisaab started."

        )

        print()

        print(

            "🐧 Battery Bhaisaab Running..."

        )

        print()

        try:

            initial = self.battery.info()

            self.previous_status = initial.status

            self.previous_capacity = initial.capacity

        except Exception:

            pass

        while True:

            try:

                self.check()

            except Exception as e:

                self.log.error(

                    f"Monitor error: {e}"

                )

            time.sleep(

                self.cfg.check_interval

            )


if __name__ == "__main__":

    BatteryMonitor().run()
