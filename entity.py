import pygame

class Entity:
    def __init__(self, x, y, w, h, name, anims):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name
        self.anims = anims
        self.action = "idle"

    def update(self, surf, dt):
        surf.blit(self.anims[self.action].play(dt))
