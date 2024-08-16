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
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] and (pos.y < 320):
                for i in range(8):
                    if (i*32 <= pos.x < (i+1)*32):
                        print("Colour clicked")

    pygame.draw.rect(screen, (255, 0, 0), (0, 320, 32, 32))
    pygame.draw.rect(screen, (0, 255, 0), (32, 320, 32, 32))
    pygame.draw.rect(screen, (0, 0, 255), (64, 320, 32, 32))
    pygame.draw.rect(screen, (255, 255, 0), (96, 320, 32, 32))
    pygame.draw.rect(screen, (0, 255, 255), (128, 320, 32, 32))
    pygame.draw.rect(screen, (255, 0, 255), (160, 320, 32, 32))
    pygame.draw.rect(screen, (255, 255, 255), (192, 320, 32, 32))
    pygame.draw.rect(screen, (0, 0, 0), (224, 320, 32, 32))

    display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick()
