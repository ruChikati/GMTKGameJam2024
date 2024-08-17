import os
import sys
import time

import pygame

from anim import Animation
from entity import Entity
from wallpaper import Wallpaper

display = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Drawn to Scale")


screen = pygame.Surface((640, 360))
clock = pygame.time.Clock()
dt = 1.0
last_time = time.time()


player = Entity(
    0, 0, 16, 16, "player", {"idle": Animation(f"anims{os.sep}player;idle")}, screen
)

tile_imgs = {}
for file in os.listdir("tiles"):
    if file.endswith(".png"):
        tile_imgs[file.split(".")[0]] = pygame.image.load(
            "tiles" + os.sep + file
        ).convert()

wallpaper = Wallpaper(screen, tile_imgs)
scroll = pygame.Vector2(0, 0)

while True:

    dt = (time.time() - last_time) * 60 * 10
    last_time = time.time()
    #print(dt)
    screen.fill((255, 248, 231))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.Vector2(pygame.mouse.get_pos())
            if pygame.mouse.get_pressed()[0] and (pos.y < 320):
                for i in range(8):
                    if i * 32 <= pos.x < (i + 1) * 32:
                        print("Colour clicked")

        if event.type == pygame.MOUSEWHEEL:
            scroll.x += 5 * event.x * -1
            scroll.y += 5 * event.y
            if 640 < scroll.x: scroll.x = 640
            if 0 > scroll.x: scroll.x = 0
            if -360 > scroll.y: scroll.y = -360
            if 0 < scroll.y: scroll.y = 0

    print(scroll)
    wallpaper.draw(scroll)

    pygame.draw.rect(screen, (255, 0, 0), (0, 360, 32, 32))
    pygame.draw.rect(screen, (0, 255, 0), (32, 360, 32, 32))
    pygame.draw.rect(screen, (0, 0, 255), (64, 360, 32, 32))
    pygame.draw.rect(screen, (255, 255, 0), (96, 360, 32, 32))
    pygame.draw.rect(screen, (0, 255, 255), (128, 360, 32, 32))
    pygame.draw.rect(screen, (255, 0, 255), (160, 360, 32, 32))
    pygame.draw.rect(screen, (255, 255, 255), (192, 360, 32, 32))
    pygame.draw.rect(screen, (0, 0, 0), (224, 360, 32, 32))

    player.update(dt)
    display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick()
