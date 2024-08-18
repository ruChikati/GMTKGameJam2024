import os
import sys
import time

import pygame

import input
from anim import Animation
from entity import Entity
from wallpaper import Wallpaper

display = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Drawn to Scale")

inputs = input.Input()
screen = pygame.Surface((320, 180))
clock = pygame.time.Clock()
dt = 1.0
last_time = time.time()

player = Entity(
    0, 0, 16, 16, "player", {"idle": Animation(f"anims{os.sep}player;idle")}, screen
)

speed = 1

tile_imgs = {}
for file in os.listdir("tiles"):
    if file.endswith(".png"):
        tile_imgs[file.split(".")[0]] = pygame.image.load(
            "tiles" + os.sep + file
        ).convert()

wallpaper = Wallpaper(
    screen,
    tile_imgs,
    offset=pygame.Vector2(-256, -512),
)
floor_tiles = []
for i in range(16):
    floor_tiles.append(pygame.Vector2(-256 + 32 * i, 0))
    floor_tiles.append(pygame.Vector2(-256 + 32 * i, 32))
    floor_tiles.append(pygame.Vector2(-256 + 32 * i, 64))
floor_surf = pygame.image.load(f".{os.sep}tiles{os.sep}brick.png")

scroll = pygame.Vector2(-152, -119)
tile_selected = (0, 0)

while True:

    dt = time.time() - last_time
    last_time = time.time()
    screen.fill((255, 248, 231))

    if scroll.x < -255:
        scroll.x = -255
    if scroll.x > -65:
        scroll.x = -65

    for event in inputs.get():
        match event.type:
            case input.QUIT:
                pygame.quit()
                sys.exit()
            case input.KEYDOWN2:
                match event.key:
                    case input.ESCAPE:
                        pygame.quit()
                        sys.exit()
            case input.KEYHOLD:
                match event.key:
                    case input.W:
                        player.move(pygame.Vector2(0, -speed))
                        scroll.y += -speed
                    case input.A:
                        player.move(pygame.Vector2(-speed, 0))
                        scroll.x += -speed
                    case input.S:
                        if player.rect.y < 16:
                            player.move(pygame.Vector2(0, speed))
                            scroll.y += speed
                    case input.D:
                        player.move(pygame.Vector2(speed, 0))
                        scroll.x += speed

    for pos in floor_tiles:
        screen.blit(floor_surf, pos - scroll)
    wallpaper.draw(scroll)
    player.update(dt, scroll)

    display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick()
