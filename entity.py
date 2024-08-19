import pygame

import anim


class Entity:
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        name: str,
        anims: dict[str : anim.Animation],
        surf: pygame.Surface,
    ):
        self.rect = pygame.Rect(x, y, w, h)
        self.name = name
        self.anims = anims
        self.action = "idle"
        self.surf = surf
        self.pos = pygame.Vector2(x, y)

    def update(self, dt: float, scroll: pygame.Vector2):
        self.rect.topleft = self.pos
        if self.anims:
            self.anims[self.action].play(dt)
            self.surf.blit(
                self.anims[self.action].get_img(), self.rect.topleft - scroll
            )

    def move(self, vec: pygame.Vector2):
        self.pos += vec

    def teleport(self, pos: pygame.Vector2):
        self.pos = pos.copy()
        self.rect.topleft = self.pos

    def change_action(self, action: str):
        self.anims[self.action].rewind()
        self.action = action
