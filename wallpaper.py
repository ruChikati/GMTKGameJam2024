import pygame


class Wallpaper:
    def __init__(
        self,
        surf: pygame.Surface,
        imgs: dict[str : pygame.Surface],
        offset: pygame.Vector2 = pygame.Vector2(0, 0),
    ):
        self.screen = surf
        self.w_tiles = []
        self.offset = offset

        for i in range(16):
            temp_arr = []
            for j in range(16):
                w = WallpaperTile(i * 32 + offset.x, j * 32 + offset.y, 32, 32)
                temp_arr.append(w)
            self.w_tiles.append(temp_arr)

        self.imgs = imgs

    def change_screen(self, surface):
        self.screen = surface

    def draw(self, scroll: pygame.Vector2, zoom: float=1):
        for i in range(len(self.w_tiles)):
            for j in range(len(self.w_tiles[i])):
                self.screen.blit(
                    pygame.transform.scale(
                        self.imgs[self.w_tiles[i][j].status], (
                            zoom*self.imgs[self.w_tiles[i][j].status].get_width(),
                            zoom*self.imgs[self.w_tiles[i][j].status].get_height()
                        )
                    ),
                    (zoom * (self.w_tiles[i][j].rect.topleft[0]) - scroll[0], zoom * (self.w_tiles[i][j].rect.topleft[1]) - scroll[1])
                )


class WallpaperTile:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.status = "white"

    def change_status(self, status: str) -> bool:
        if status == self.status:
            return False
        self.status = status
        return True
