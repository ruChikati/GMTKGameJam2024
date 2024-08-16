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

    def update(self, dt: float):
        self.anims[self.action].play(dt)
        self.surf.blit(self.anims[self.action].get_img(), self.rect.topleft)

    def mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.x - 5 < pos[0] < self.x + 5 and self.y - 5 < pos[1] < self.y + 5:
                if pygame.mouse.get_pressed()[0]:
                    return 1 # Right click
                elif pygame.mouse.get_pressed()[1]:
                    return -1 # Left click
        return 0 # No mouse event

    def change_action(self, action: str):
        self.anims[self.action].rewind()
        self.action = action
