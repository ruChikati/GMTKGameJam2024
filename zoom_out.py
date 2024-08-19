import pygame


class ZoomOut:
    def __init__(self, screen, surface, player, wallpaper):
        self.screen = screen
        self.surface = surface
        self.zoomed_surface = pygame.Surface(self.screen.get_size())
        self.player = player
        self.wallpaper = wallpaper

        self.wallpaper.change_screen(self.zoomed_surface)

        self.zoom = 0.1

    def draw(self, scroll, floor_tiles):
        for surf_pos in floor_tiles:
            self.zoomed_surface.blit(surf_pos[1], surf_pos[0] - scroll)
        scaled_zoom_surface = pygame.transform.scale(self.zoomed_surface, (self.zoom * self.surface.get_width(), self.zoom * self.surface.get_height()))
        self.surface.blit(scaled_zoom_surface, scaled_zoom_surface.get_rect())
        scaled_surface = pygame.transform.scale(self.surface, self.screen.get_size())
        self.screen.blit(scaled_surface, scaled_surface.get_rect())
