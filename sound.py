import os
import random

import pygame

pygame.mixer.pre_init(44100, -16, 6, 512)
pygame.mixer.init()


class SFXManager:
    def __init__(self, num_channels: int = 63):

        self.path = f".{os.sep}sounds{os.sep}sfx{os.sep}"
        self.sfx_enabled = True
        self.sounds = {}
        self.music = {}
        self.paused = False
        self.queue = []
        for file in os.listdir(f"{self.path}sounds"):
            if "." not in file:
                self.sounds[file] = [
                    pygame.mixer.Sound(
                        f"{self.path}sounds{os.sep}{file}{os.sep}{sound}"
                    )
                    for sound in os.listdir(f"{self.path}sounds{os.sep}{file}")
                    if sound[0] != "."
                ]
                # sounds are stored in a directory which is stored in `path`
        for file in os.listdir(f"{self.path}music"):
            if "." not in file:
                self.music[file] = [
                    music
                    for music in os.listdir(f"{self.path}music{os.sep}{file}")
                    if music[0] != "."
                ]
        self.num_channels = num_channels

    def adjust_volume(self, name: str, vol: float):  # vol in [0, 1]
        for i in self.sounds[name]:
            i.set_volume(vol)

    @staticmethod
    def adjust_bgm_volume(vol: float):
        pygame.mixer.music.set_volume(vol)

    def play(self, name: str, loops: int = 0, maxtime: int = 0, fade_ms: int = 0):
        if self.sfx_enabled:
            try:
                pygame.mixer.find_channel().play(
                    random.choice(self.sounds[name]), loops, maxtime, fade_ms
                )
            except (KeyError, AttributeError):
                pass

    def toggle_sound(self, toggle: bool):
        self.sfx_enabled = toggle

    def start_music(self, repeat: int = -1): # repeat = -1 plays indefinitely
        if self.queue:
            pygame.mixer.music.load(self.queue[0])
            pygame.mixer.music.play(repeat)

    def update(self):
        if not (pygame.mixer.music.get_busy() or self.paused):
            if self.queue:
                del self.queue[0]
                pygame.mixer.music.load(self.queue[0])
                pygame.mixer.music.play()
            elif len(self.queue) == 1:
                del self.queue[0]

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def unpause_music(self):
        pygame.mixer.music.unpause()
        self.paused = False

    def stop(self, name: str):
        for sound in self.sounds[name]:
            sound.stop()

    def new_sound(self, path: str):
        self.sounds[path] = [
            pygame.mixer.Sound(sound) for sound in os.listdir(path) if sound[0] != "."
        ]

    def add_queue(self, music: str):
        self.queue.append(music)

    @staticmethod
    def stop_all():
        pygame.mixer.stop()

    @property
    def num_channels(self):
        return pygame.mixer.get_num_channels()

    @num_channels.setter
    def num_channels(self, num: int):
        pygame.mixer.set_num_channels(num)
