import pygame

import anim


class Entity:
    def __init__(self, x: int, y: int, w: int, h: int, name: str, anims: dict[str : anim.Animation]):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name
        self.anims = anims
        self.action = "idle"

    def update(self, surf: pygame.Surface, dt: float):
        surf.blit(self.anims[self.action].play(dt), (self.x, self.y))
