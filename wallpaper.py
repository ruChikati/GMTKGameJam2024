import pygame


class WallpaperTile:
    def __init__(self, x, y, width, height, tile_size, filename):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(filename)

        self.tile_size = tile_size

        self.w_tiles = []

    def load_tiles(self):
        n = self.rect.width // self.tile_size
        m = self.rect.height // self.tile_size

        for i in range(n):
            temp_arr = []
            for j in range(m):
                temp_arr.append(
                    self.image.subsurface(
                        i * self.rect.width,
                        j * self.rect.height,
                        self.rect.width,
                        self.rect.height,
                    )
                )

            self.w_tiles.append(temp_arr)

    def draw(self, surface_coordinate):
        for i in range(len(self.image)):
            for j in range(len(self.image[i])):
                self.screen.blit(self.screen, (i * width + 1, j * height + 1))
