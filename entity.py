import pygame

class Entity:
    def __init__(self, x, y, w, h, name, display, img_path):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name
        self.display = display
        self.image = pygame.image.load(img_path)
        pygame.transform.scale(self.image, (self.w, self.h))

    def update(self, dt):
        self.display.blit(self.image, (self.x, self.y))