import os
import sys
import time

import pygame

import input
from anim import Animation
from entity import Entity
from wallpaper import Wallpaper
from sound import SFXManager

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

sfxman = SFXManager()
sfxman.adjust_volume("paint", 0.05)
sfxman.add_queue(f".{os.sep}sounds{os.sep}sfx{os.sep}music{os.sep}" + os.listdir(f".{os.sep}sounds{os.sep}sfx{os.sep}music{os.sep}")[0])
sfxman.adjust_bgm_volume(0.1)
sfxman.start_music()

scroll = pygame.Vector2(-152, -119)
tile_selected = pygame.Vector2(0, 0)

while True:

    dt = time.time() - last_time
    last_time = time.time()
    screen.fill((255, 248, 231))

    if scroll.x < -255:
        scroll.x = -255
    if scroll.x > -70:
        scroll.x = -70
    if scroll.y > -103:
        scroll.y = -103
    if scroll.y < -512:
        scroll.y = -512

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
                        if player.rect.y > -512:
                            player.move(pygame.Vector2(0, -speed))
                            scroll.y += -speed
                    case input.A:
                        if player.rect.x > -256:
                            player.move(pygame.Vector2(-speed, 0))
                    case input.S:
                        if player.rect.y < 16:
                            player.move(pygame.Vector2(0, speed))
                            scroll.y += speed
                    case input.D:
                        if player.rect.x < 240:
                            player.move(pygame.Vector2(speed, 0))
                    case input.SPACE:
                        sfxman.play("paint")
                        for i in range(16):
                            for j in range(16):
                                try:
                                    if player.rect.colliderect(wallpaper.w_tiles[i][j].rect):
                                        tile_selected = pygame.Vector2(i, j)
                                        del wallpaper.w_tiles[i][j] # TODO: change colour of tile
                                except IndexError:
                                    pass

    if player.rect.right > screen.get_width() // 2 + scroll.x + 152:
        scroll.x += speed
    if (
        player.rect.left - 10 < -screen.get_width() // 2 + scroll.x + 152
    ):  # - 10 just works, idk why
        scroll.x += -speed
    if player.rect.top < screen.get_height() // 2 + scroll.y + 119:
        scroll.y += -speed
    if player.rect.bottom > -screen.get_height() // 2 + scroll.y + 119:
        scroll.y += speed

    for pos in floor_tiles:
        screen.blit(floor_surf, pos - scroll)
    wallpaper.draw(scroll)
    pygame.draw.rect(screen, (255, 0, 0), wallpaper.w_tiles[int(tile_selected.x)][int(tile_selected.y)].rect, 1) ## FIXME: doesnt work
    player.update(dt, scroll)

    display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick()
