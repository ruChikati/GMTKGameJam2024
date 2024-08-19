import os
import sys
import time

import pygame

import input
from anim import Animation
from entity import Entity
from sound import SFXManager
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
paint = {
    "red": Entity(
        -64, 16, 8, 16, "red", {"idle": Animation(f"anims{os.sep}red;idle")}, screen
    ),
    "green": Entity(
        -48, 16, 8, 16, "green", {"idle": Animation(f"anims{os.sep}green;idle")}, screen
    ),
    "blue": Entity(
        -32, 16, 8, 16, "blue", {"idle": Animation(f"anims{os.sep}blue;idle")}, screen
    ),
    "cyan": Entity(
        -16, 16, 8, 16, "cyan", {"idle": Animation(f"anims{os.sep}cyan;idle")}, screen
    ),
    "magenta": Entity(
        0,
        16,
        8,
        16,
        "magenta",
        {"idle": Animation(f"anims{os.sep}magenta;idle")},
        screen,
    ),
    "yellow": Entity(
        16,
        16,
        8,
        16,
        "yellow",
        {"idle": Animation(f"anims{os.sep}yellow;idle")},
        screen,
    ),
    "black": Entity(
        32, 16, 8, 16, "black", {"idle": Animation(f"anims{os.sep}black;idle")}, screen
    ),
    "white": Entity(
        48, 16, 8, 16, "white", {"idle": Animation(f"anims{os.sep}white;idle")}, screen
    ),
}

speed = 1
selected_colour = "blue"

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
floor_surf = pygame.image.load(f".{os.sep}tiles{os.sep}brick.png")

for i in range(16):
    floor_tiles.append((pygame.Vector2(-256 + 32 * i, 0), floor_surf))
    floor_tiles.append((pygame.Vector2(-256 + 32 * i, 32), floor_surf))
    floor_tiles.append((pygame.Vector2(-256 + 32 * i, 64), floor_surf))

sfxman = SFXManager()
sfxman.adjust_volume("paint", 0.1)
sfxman.add_queue(
    f".{os.sep}sounds{os.sep}sfx{os.sep}music{os.sep}"
    + os.listdir(f".{os.sep}sounds{os.sep}sfx{os.sep}music{os.sep}")[0]
)
sfxman.adjust_bgm_volume(0.1)
sfxman.start_music()

OFFSET = pygame.Vector2(152, 119)
scroll = -OFFSET

while True:

    dt = time.time() - last_time
    last_time = time.time()
    screen.fill((255, 248, 231))

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
                        if player.pos.y > -512:
                            player.move(pygame.Vector2(0, -speed))
                    case input.A:
                        if player.pos.x > -256:
                            player.move(pygame.Vector2(-speed, 0))
                    case input.S:
                        if player.pos.y < 16:
                            player.move(pygame.Vector2(0, speed))
                    case input.D:
                        if player.pos.x < 240:
                            player.move(pygame.Vector2(speed, 0))
            case input.KEYDOWN:
                match event.key:
                    case input.E:
                        for colour in paint:
                            if (
                                paint[colour].rect.colliderect(player.rect)
                                and colour != selected_colour
                            ):
                                sfxman.play("bucket")
                                selected_colour = colour
                                break
                    case input.SPACE:
                        if player.pos.y <= 0:
                            sfxman.play("paint", 2)
                            for i in range(16):
                                for j in range(16):
                                    try:
                                        if player.rect.colliderect(
                                            wallpaper.w_tiles[i][j].rect
                                        ):
                                            wallpaper.w_tiles[i][j].change_status(
                                                selected_colour
                                            )
                                            break
                                    except IndexError:
                                        pass

    if player.rect.right - scroll.x > screen.get_width() // 2:
        scroll.x += speed
    if player.rect.left - scroll.x < screen.get_width() // 2:
        scroll.x += -speed
    if player.rect.top - scroll.y < screen.get_height() // 2:
        scroll.y += -speed
    if player.rect.bottom - scroll.y > screen.get_height() // 2:
        scroll.y += speed

    if scroll.x < -255:
        scroll.x = -255
    if scroll.x > -70:
        scroll.x = -70
    if scroll.y > -103:
        scroll.y = -103
    if scroll.y < -512:
        scroll.y = -512

    for surf_pos in floor_tiles:
        screen.blit(surf_pos[1], surf_pos[0] - scroll)
    wallpaper.draw(scroll)

    paint[selected_colour].teleport(player.pos)
    for e in paint.values():
        e.update(dt, scroll)
    player.update(dt, scroll)
    display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick()
