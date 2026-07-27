#!/usr/bin/env python3

"""
Battery Bhaisaab

Configuration Manager
"""

from configparser import ConfigParser
from paths import CONFIG_DIR, CONFIG_FILE


DEFAULT_CONFIG = """[GENERAL]
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
"""


class Config:

    def __init__(self):

        CONFIG_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        if not CONFIG_FILE.exists():

            CONFIG_FILE.write_text(
                DEFAULT_CONFIG
            )

        self.parser = ConfigParser()

        self.parser.read(CONFIG_FILE)

    # -----------------------------------------------------

    @property
    def check_interval(self):

        return self.parser.getint(
            "GENERAL",
            "check_interval"
        )

    @property
    def logging(self):

        return self.parser.getboolean(
            "GENERAL",
            "logging"
        )

    # -----------------------------------------------------

    @property
    def level1(self):

        return self.parser.getint(
            "BATTERY",
            "level1"
        )

    @property
    def level2(self):

        return self.parser.getint(
            "BATTERY",
            "level2"
        )

    @property
    def level3(self):

        return self.parser.getint(
            "BATTERY",
            "level3"
        )

    @property
    def level4(self):

        return self.parser.getint(
            "BATTERY",
            "level4"
        )

    # -----------------------------------------------------

    @property
    def notifications(self):

        return self.parser.getboolean(
            "NOTIFICATIONS",
            "enabled"
        )

    @property
    def notification_timeout(self):

        return self.parser.getint(
            "NOTIFICATIONS",
            "timeout"
        )

    @property
    def low_battery_notifications(self):

        return self.parser.getboolean(
            "NOTIFICATIONS",
            "low_battery",
            fallback=True
        )

    @property
    def charger_connected_notifications(self):

        return self.parser.getboolean(
            "NOTIFICATIONS",
            "charger_connected",
            fallback=True
        )

    @property
    def charger_removed_notifications(self):

        return self.parser.getboolean(
            "NOTIFICATIONS",
            "charger_removed",
            fallback=True
        )

    @property
    def battery_full_notifications(self):

        return self.parser.getboolean(
            "NOTIFICATIONS",
            "battery_full",
            fallback=True
        )

    # -----------------------------------------------------

    @property
    def audio(self):

        return self.parser.getboolean(
            "AUDIO",
            "enabled"
        )
