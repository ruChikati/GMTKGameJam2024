import pygame


BLANK = (255, 248, 231)
DIRTY = (100, 100, 100)
MOSS = (50, 200, 50)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
COMPLETE = (0, 0, 0)


class Wallpaper:
    def __init__(self, surface, wallpaper_tiles):
        self.screen = surface
        self.w_tiles = wallpaper_tiles

    def draw(self):
        for i in range(len(self.w_tiles)):
            for j in range(len(self.w_tiles[i])):
                pygame.draw.rect(self.screen, self.w_tiles[i][j].status, self.w_tiles[i][j].rect)


class WallpaperTile:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

        self.status = BLANK

    def draw(self, surface):
        pygame.draw.rect(screen, self.status, self.rect)
