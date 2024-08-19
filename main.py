import os
import sys
import time
from random import shuffle

import pygame

import input
from anim import Animation
from entity import Entity
from start import sfxman, start, artwork_surf
from wallpaper import Wallpaper
from widgets import Button

start()

display = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Drawn to Scale")

inputs = input.Input()
screen = pygame.Surface((320, 180))
clock = pygame.time.Clock()
dt = 1.0
last_time = time.time()

sfxman.adjust_volume("bucket", 0.2)

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
    "": Entity(0, 0, 0, 0, "", {}, screen),
}

face_left = False

speed = 0.5
gravity = pygame.Vector2(0, 0.25)
selected_colour = ""
on_ladder = False  # TODO: add ladder mechanics

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

OFFSET = pygame.Vector2(152, 119)
scroll = -OFFSET
zoom = 1

finished_painting = False

font = pygame.font.SysFont(None, 30)
toggle_img = Button(display, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Toggle Image", (183, 183, 183),
                              int(-100 - scroll.x), int(150 + scroll.y),
                              140, 32)
display_image = False

while True:

    dt = time.time() - last_time
    if not finished_painting:
        last_time = time.time()
    screen.fill((255, 248, 231))

    for event in inputs.get():
        mpos = pygame.mouse.get_pos()
        if (52 <= mpos[0] <= 190 and 31 <= mpos[1] <= 61) and pygame.mouse.get_pressed()[0]:
            print("reached")
            display_image = not display_image
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
                            face_left = True
                    case input.S:
                        if player.pos.y < 16:
                            player.move(pygame.Vector2(0, speed))
                    case input.D:
                        if player.pos.x < 240:
                            player.move(pygame.Vector2(speed, 0))
                            face_left = False
            case input.KEYDOWN:
                match event.key:
                    case input.E:
                        c_before = selected_colour + "."
                        colours = list(paint.keys())
                        shuffle(colours)
                        for colour in colours:
                            if (
                                paint[colour].rect.colliderect(player.rect)
                                and colour != selected_colour
                            ):
                                sfxman.play("bucket")
                                selected_colour = colour
                                break
                        if selected_colour == c_before[:-1]:
                            selected_colour = ""
                    case input.SPACE:
                        if player.pos.y <= 0:
                            for i in range(16):
                                for j in range(16):
                                    try:
                                        if (
                                            player.rect.colliderect(
                                                wallpaper.w_tiles[i][j].rect
                                            )
                                            and selected_colour
                                        ):
                                            if (
                                                wallpaper.w_tiles[i][j].change_status(
                                                    selected_colour
                                                )
                                                and selected_colour
                                            ):
                                                sfxman.play("paint", 2)
                                    except IndexError:
                                        pass
                    case input.RETURN:
                        finished_painting = True
                        scroll = -OFFSET

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
    if scroll.x > -50:
        scroll.x = -50
    if scroll.y > -103:
        scroll.y = -103
    if scroll.y < -512:
        scroll.y = -512

    for e in paint.values():
        e.move(gravity)
        if e.pos.y >= 16:
            e.teleport(pygame.Vector2(e.pos.x, 16))

    for surf_pos in floor_tiles:
        screen.blit(pygame.transform.scale(surf_pos[1], (zoom * surf_pos[1].get_width(), zoom * surf_pos[1].get_height())), zoom * surf_pos[0] - scroll)

    if not finished_painting:
        wallpaper.draw(scroll)

        paint[selected_colour].teleport(player.pos)
        for e in paint.values():
            if e.name != selected_colour:
                e.update(dt, scroll)
        paint[selected_colour].update(dt, scroll)
        player.update(dt, scroll, face_left=face_left)

        display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    else:
        wallpaper.draw(scroll, zoom)

        if dt > 0.1 and zoom > 0.5:
            zoom -= 0.01
            last_time = time.time()

        scaled_image = pygame.transform.scale(screen, (zoom * screen.get_width(), zoom * screen.get_height()))
        display.blit(pygame.transform.scale(scaled_image, display.get_size()), (0, 0))
        player.update(dt, scroll, face_left=face_left)
        display_image = True


    toggle_img.render()
    if display_image:
        display.blit(artwork_surf, (52, 62))
    pygame.display.flip()
    clock.tick()
