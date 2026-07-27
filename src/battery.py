#!/usr/bin/env python3
"""
Battery Bhaisaab
----------------

Battery detection and information module.

This module is responsible only for interacting with
/sys/class/power_supply.

It does NOT send notifications.
It does NOT play sounds.

Author: Battery Bhaisaab Project
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional


POWER_SUPPLY_PATH = Path("/sys/class/power_supply")


class BatteryNotFoundError(Exception):
    """Raised when no battery is detected."""
    pass


@dataclass
class BatteryInfo:
    """
    Represents current battery information.
    """

    name: str
    capacity: int
    status: str

    energy_now: Optional[int] = None
    energy_full: Optional[int] = None

    power_now: Optional[int] = None

    voltage_now: Optional[int] = None

    technology: Optional[str] = None

    manufacturer: Optional[str] = None

    model_name: Optional[str] = None


class Battery:

    def __init__(self):

        self.path = self._find_battery()

    def _find_battery(self) -> Path:

        if not POWER_SUPPLY_PATH.exists():
            raise BatteryNotFoundError(
                "/sys/class/power_supply not found."
            )

        batteries = sorted(
            p for p in POWER_SUPPLY_PATH.iterdir()
            if p.name.startswith("BAT")
        )

        if not batteries:
            raise BatteryNotFoundError(
                "No battery found."
            )

        return batteries[0]

    def _read(self, filename: str):

        file = self.path / filename

        if not file.exists():
            return None

        try:
            return file.read_text().strip()

        except Exception:
            return None

    def _read_int(self, filename: str):

        value = self._read(filename)

        if value is None:
            return None

        try:
            return int(value)

        except ValueError:
            return None

    def info(self) -> BatteryInfo:

        return BatteryInfo(

            name=self.path.name,

            capacity=self._read_int("capacity") or 0,

            status=self._read("status") or "Unknown",

            energy_now=self._read_int("energy_now"),

            energy_full=self._read_int("energy_full"),

            power_now=self._read_int("power_now"),

            voltage_now=self._read_int("voltage_now"),

            technology=self._read("technology"),

            manufacturer=self._read("manufacturer"),

            model_name=self._read("model_name"),
        )

    def percentage(self) -> int:

        return self.info().capacity

    def status(self) -> str:

        return self.info().status

    def is_charging(self) -> bool:

        return self.status() == "Charging"

    def is_discharging(self) -> bool:

        return self.status() == "Discharging"

    def is_full(self) -> bool:

        return self.status() == "Full"

    def remaining_minutes(self):

        info = self.info()

        if (
            info.energy_now is None
            or info.power_now is None
            or info.power_now == 0
        ):
            return None

        hours = info.energy_now / info.power_now

        return int(hours * 60)

    def summary(self):

        info = self.info()

        return {
            "Battery": info.name,
            "Percentage": info.capacity,
            "Status": info.status,
            "Technology": info.technology,
            "Manufacturer": info.manufacturer,
            "Model": info.model_name,
            "RemainingMinutes": self.remaining_minutes(),
        }


if __name__ == "__main__":

    battery = Battery()

    print()

    print("Battery Bhaisaab")

    print("----------------")

    print()

    for key, value in battery.summary().items():

        print(f"{key:20}: {value}")
