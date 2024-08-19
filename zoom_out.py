import pygame


class ZoomOut:
    def __init__(self, screen: pygame.Surface, surface: pygame.Surface, player, wallpaper):
        self.screen = screen
        self.surface = surface
        self.zoomed_surface = pygame.Surface(self.screen.get_size())
        self.player = player
        self.wallpaper = wallpaper

        self.wallpaper.change_screen(self.zoomed_surface)

    def draw(self):
        self.surface.blit(self.zoomed_surface, (0, 0))
        self.screen.blit(self.surface, (0, 0))
