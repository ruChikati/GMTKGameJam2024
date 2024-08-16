import pygame


class Wallpaper:
    def __init__(self, surf: pygame.Surface, imgs: dict[str : pygame.Surface]):
        self.screen = surf
        self.w_tiles = []
        self.imgs = imgs

    def draw(self, scroll: pygame.Vector2):
        for i in range(len(self.w_tiles)):
            for j in range(len(self.w_tiles[i])):
                self.screen.blit(
                    self.imgs[self.w_tiles[i][j].status],
                    self.w_tiles[i][j].rect.topleft + scroll,
                )


class WallpaperTile:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.status = "b"

    def change_status(self, status: str):
        self.status = status
