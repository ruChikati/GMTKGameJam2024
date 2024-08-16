import sys

import pygame

from wallpaper import *

display = pygame.display.set_mode((640, 360))
pygame.display.set_caption("Drawn to Scale")

screen = pygame.Surface((640, 360))
clock = pygame.time.Clock()

blank_surf = pygame.Surface((32, 32))
blank_surf.fill((255, 248, 231))
wallpaper = Wallpaper(screen, {"b": blank_surf})

scroll = pygame.Vector2(0, 0)

while True:

    #screen.fill((255, 248, 231))
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] and (pos.y < 320):
                for i in range(8):
                    if (i*32 <= pos.x < (i+1)*32):
                        print("Colour clicked")

        if event.type == pygame.MOUSEWHEEL:
            scroll.y += 5 * event.y
            scroll.x += 5 * event.x * -1

    wallpaper.draw(scroll)


    pygame.draw.rect(screen, (255, 0, 0), (0, 360, 32, 32))
    pygame.draw.rect(screen, (0, 255, 0), (32, 360, 32, 32))
    pygame.draw.rect(screen, (0, 0, 255), (64, 360, 32, 32))
    pygame.draw.rect(screen, (255, 255, 0), (96, 360, 32, 32))
    pygame.draw.rect(screen, (0, 255, 255), (128, 360, 32, 32))
    pygame.draw.rect(screen, (255, 0, 255), (160, 360, 32, 32))
    pygame.draw.rect(screen, (255, 255, 255), (192, 360, 32, 32))
    pygame.draw.rect(screen, (0, 0, 0), (224, 360, 32, 32))

    display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick()
