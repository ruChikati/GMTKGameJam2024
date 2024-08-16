import os

import pygame

from utils import FileTypeError, LengthError, read_json, sum_list, write_json


class Animation:
    def __init__(self, path: str):
        self.path = path
        self.frame_paths = os.listdir(self.path)
        self.frame = 0
        self.frame_paths.sort()
        self.paused = False
        try:
            self.config = read_json(f"{self.path}{os.sep}config.json")
        except FileNotFoundError:
            self.config = {
                "frames": [5] * len(self.frame_paths),
                "speed": 1.0,
                "loop": False,
            }
            write_json(f"{self.path}{os.sep}config.json", self.config)
        self.frame_durations = sum_list(self.config["frames"])
        self.frames = []
        for frame in self.frame_paths:
            if frame.split(".")[-1] == "png":
                frame = pygame.image.load(f"{self.path}{os.sep}{frame}").convert_alpha()
                frame.set_colorkey((1, 1, 1))
                self.frames.append(frame)
            elif frame.split(".")[-1] == "json":
                pass
            else:
                raise FileTypeError(frame.split(".")[-1])
        if len(self.frames) > len(self.frame_paths) + 1:
            self.config["frames"] += [5] * (len(self.frames) - len(self.frame_paths))
        elif len(self.frames) < (len(self.frame_paths) - 1):
            raise LengthError("Not enough frames in animation")
        self._calcualate_img()

    def _calcualate_img(self):
        if len(self.frames) != len(self.frame_durations):
            raise LengthError(
                "frame_durations does not have the same length as frames in "
                + self.path
                + "'s animation"
            )
        for frame, t in zip(self.frames, self.frame_durations):
            if t > self.frame:
                self._img = frame
                break
        if self.frame_durations[-1] < self.frame:
            self._img = self.frames[-1]

    def play(self, dt: float, fps=60) -> int:
        if not self.paused:
            self.frame += dt * fps * self.config["speed"]
        if self.config["loop"]:
            if self.frame > self.duration:
                self.frame = 0
        self._calcualate_img()
        return self.frame

    def get_img(self):
        return self._img

    def rewind(self, index=0):
        self.frame = index

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    @property
    def duration(self):
        return sum(self.config["frames"])
