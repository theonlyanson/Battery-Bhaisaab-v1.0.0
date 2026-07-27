#!/usr/bin/env python3
"""
Battery Bhaisaab
----------------
Audio Engine

Automatically detects an available audio player and
plays notification sounds.

Supported players (in priority order):

- paplay
- pw-play
- mpv
- ffplay
- play (SoX)
- aplay
"""

from pathlib import Path
import shutil
import subprocess


class AudioError(Exception):
    pass


class Audio:

    PLAYERS = [
        "paplay",
        "pw-play",
        "mpv",
        "ffplay",
        "play",
        "aplay"
    ]

    def __init__(self):

        self.player = self.detect_player()

    def detect_player(self):

        for player in self.PLAYERS:

            if shutil.which(player):
                return player

        return None

    def available(self):

        return self.player is not None

    def player_name(self):

        return self.player

    def play(self, sound):

        if self.player is None:
            raise AudioError("No supported audio player found.")

        sound = Path(sound)

        if not sound.exists():
            raise AudioError(f"Sound file not found: {sound}")

        cmd = self._command(sound)

        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _command(self, sound):

        sound = str(sound)

        if self.player == "paplay":
            return ["paplay", sound]

        elif self.player == "pw-play":
            return ["pw-play", sound]

        elif self.player == "mpv":
            return [
                "mpv",
                "--really-quiet",
                "--no-video",
                sound
            ]

        elif self.player == "ffplay":
            return [
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "quiet",
                sound
            ]

        elif self.player == "play":
            return ["play", sound]

        elif self.player == "aplay":
            return ["aplay", sound]

        raise AudioError("Unsupported player.")


if __name__ == "__main__":

    audio = Audio()

    print()

    print("Battery Bhaisaab Audio")

    print("----------------------")

    if audio.available():

        print("Player Detected :", audio.player_name())

    else:

        print("No audio player found.")
