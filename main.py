import sys

import pygame

display = pygame.display.set_mode((640, 360))
screen = pygame.Surface((640, 360))
clock = pygame.time.Clock()

while True:

    screen.fill((255, 248, 231))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick()
