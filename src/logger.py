#!/usr/bin/env python3

"""
Battery Bhaisaab

Logging Engine
"""

from datetime import datetime
from paths import LOG_DIR


class Logger:

    def __init__(self):

        LOG_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.log_dir = LOG_DIR
        self.log_file = self.log_dir / "battery.log"

    # -----------------------------------------------------

    def write(self, level, message):

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        line = f"{now} [{level}] {message}\n"

        with self.log_file.open(
            "a",
            encoding="utf-8"
        ) as f:

            f.write(line)

    # -----------------------------------------------------

    def info(self, message):

        self.write("INFO", message)

    # -----------------------------------------------------

    def warning(self, message):

        self.write("WARNING", message)

    # -----------------------------------------------------

    def error(self, message):

        self.write("ERROR", message)

    # -----------------------------------------------------

    def last(self, lines=20):

        if not self.log_file.exists():
            return []

        with self.log_file.open(
            encoding="utf-8"
        ) as f:

            return f.readlines()[-lines:]
