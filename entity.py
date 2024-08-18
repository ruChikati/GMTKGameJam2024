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

    def update(self, dt: float, scroll: pygame.Vector2):
        self.anims[self.action].play(dt)
        self.surf.blit(self.anims[self.action].get_img(), self.rect.topleft - scroll)

    def move(self, vec: pygame.Vector2):
        self.rect.topleft += vec

    def change_action(self, action: str):
        self.anims[self.action].rewind()
        self.action = action
