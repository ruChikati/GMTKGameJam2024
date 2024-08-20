import importlib
import os
import sys
import time
from random import shuffle

import pygame

import input
from anim import Animation
from entity import Entity
from start import artwork, artwork_surf, sfxman, start
from wallpaper import Wallpaper
from widgets import Button, Label


# from PIL import Image


def evaluate_img(wp: Wallpaper, art_scaled_down: pygame.Surface) -> int:
    cols = {
        0xFF0000FF: "red",
        0x00FF00FF: "green",
        0x0000FFFF: "blue",
        0x00FFFFFF: "cyan",
        0xFF00FFFF: "magenta",
        0xFFFF00FF: "yellow",
        0x000000FF: "black",
        0xFFFFFFFF: "white",
    }
    art_score = 0
    if art_scaled_down.get_size() != (16, 16):
        raise ValueError("art file not the correct size")
    for x in range(16):
        for y in range(16):
            if cols[int(art_scaled_down.get_at((x, y)))] == wp.w_tiles[x][y].status:
                art_score += 1

    return art_score


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
    0,
    16,
    16,
    16,
    "player",
    {
        "idle": Animation(f"anims{os.sep}player;idle"),
        "walk": Animation(f"anims{os.sep}player;walk"),
    },
    screen,
)
ladder = Entity(
    100,
    -800,
    32,
    820,
    "ladder",
    {"idle": Animation(f"anims{os.sep}ladder;idle")},
    screen,
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

player_speed = 0.5
gravity = pygame.Vector2(0, 0.25)
selected_colour = ""
on_ladder = False
ladder_selected = False

tile_imgs = {}
for file in os.listdir("tiles"):
    if file.endswith(".png"):
        tile_imgs[file.split(".")[0]] = pygame.image.load(
            "tiles" + os.sep + file
        ).convert()
coloured = False

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
toggle_img = Button(
    display,
    (180, 20, 10),
    (180, 80, 10),
    (10, 75, 20),
    font,
    "Toggle Image",
    (183, 183, 183),
    int(-100 - scroll.x),
    int(150 + scroll.y),
    140,
    32,
)
display_image = False

score = -1
screenshot_rect = pygame.Rect(int(400 - OFFSET.x), int(-100 + OFFSET.y), 1000, 650)
score_l = Label(
    display,
    font,
    "Score: " + str(score),
    (255, 0, 0),
    int(200 - OFFSET.x),
    int(550 + OFFSET.y),
    100,
    10,
)

replay = Button(
    display,
    (180, 20, 10),
    (180, 80, 10),
    (10, 75, 20),
    font,
    "Replay",
    (183, 183, 183),
    48,
    575,
    140,
    32,
)

while True:

    dt = time.time() - last_time
    if not finished_painting:
        last_time = time.time()
    screen.fill((255, 248, 231))

    on_ladder = player.rect.colliderect(ladder.rect)

    for event in inputs.get():
        mpos = pygame.mouse.get_pos()
        if (
            52 <= mpos[0] <= 190 and 31 <= mpos[1] <= 61
        ) and pygame.mouse.get_pressed()[0]:
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
                        if (
                            (player.pos.y > -512 and on_ladder or player.pos.y > -16)
                            and not ladder_selected
                            and not finished_painting
                        ):
                            player.move(pygame.Vector2(0, -player_speed))
                        if finished_painting:
                            player.move(pygame.Vector2(0, -player_speed))
                    case input.A:
                        if (
                            player.pos.x > -256
                            and player.pos.y >= -16
                            and not finished_painting
                        ):
                            player.move(pygame.Vector2(-player_speed, 0))
                            face_left = True
                            player.change_action("walk")
                        if finished_painting:
                            player.move(pygame.Vector2(-player_speed, 0))
                    case input.S:
                        if (
                            (
                                player.pos.y < 16
                                and on_ladder
                                or player.pos.y >= -16
                                and not player.pos.y > 16
                            )
                            and not ladder_selected
                            and not finished_painting
                        ):
                            player.move(pygame.Vector2(0, player_speed))
                        if finished_painting:
                            player.move(pygame.Vector2(0, player_speed))
                    case input.D:
                        if (
                            player.pos.x < 240
                            and player.pos.y >= -16
                            and not finished_painting
                        ):
                            player.move(pygame.Vector2(player_speed, 0))
                            face_left = False
                            player.change_action("walk")
                        if finished_painting:
                            player.move(pygame.Vector2(player_speed, 0))

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
                    case input.R:
                        if on_ladder and player.pos.y >= -16:
                            ladder_selected = not ladder_selected
                    case input.SPACE:
                        coloured = False
                        if player.pos.y <= 0:
                            for i in range(16):
                                for j in range(16):
                                    try:
                                        if (
                                            not coloured
                                            and player.rect.colliderect(
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
                                                coloured = True
                                    except IndexError:
                                        pass
                    case input.RETURN:
                        finished_painting = True
                        scroll = -OFFSET
                        player.pos = pygame.Vector2(0, 0)
                    case input.Q:
                        display_image = not display_image
            case input.KEYUP:
                match event.key:
                    case input.A | input.D:
                        player.change_action("idle")
            case input.MOUSEDOWN:
                if finished_painting:
                    if replay.handle_event(event, mpos):
                        import main
                        importlib.reload(main)

    if player.rect.right - scroll.x > screen.get_width() // 2:
        scroll.x += player_speed
    if player.rect.left - scroll.x < screen.get_width() // 2:
        scroll.x += -player_speed
    if player.rect.top - scroll.y < screen.get_height() // 2:
        scroll.y += -player_speed
    if player.rect.bottom - scroll.y > screen.get_height() // 2:
        scroll.y += player_speed

    if scroll.x < -255:
        scroll.x = -255
    if scroll.x > -50:
        scroll.x = -50
    if scroll.y > -103:
        scroll.y = -103
    if scroll.y < -512:
        scroll.y = -512

    for e in paint.values():
        if e.pos.y < 16:
            e.move(gravity)
    if ladder_selected:
        ladder.teleport(player.pos - pygame.Vector2(0, 816))

    for surf_pos in floor_tiles:
        screen.blit(
            pygame.transform.scale(
                surf_pos[1], zoom * pygame.Vector2(surf_pos[1].get_size())
            ),
            zoom * surf_pos[0] - scroll,
        )

    wallpaper.draw(scroll, zoom)

    if not finished_painting:
        paint[selected_colour].teleport(player.pos)
        for e in paint.values():
            if e.name != selected_colour:
                e.update(dt, scroll)
        paint[selected_colour].update(dt, scroll)
        ladder.update(dt, scroll)
        player.update(dt, scroll, face_left=face_left)
        display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    else:
        if dt > 0.1 and zoom > 0.4:
            zoom -= 0.1
            last_time = time.time()

        scaled_image = pygame.transform.scale(
            screen, (zoom * screen.get_width(), zoom * screen.get_height())
        )
        display.blit(pygame.transform.scale(scaled_image, display.get_size()), (0, 0))
        player.update(dt, scroll, face_left=face_left)
        display_image = True

    if finished_painting:
        pygame.draw.rect(display, (255, 0, 0), screenshot_rect, 3)
        score_l.text = "Score: " + str(score)
        score_l.render()

    toggle_img.render()
    if display_image:
        display.blit(artwork_surf, (52, 62))

    if finished_painting:
        player_speed = 10
        if score < -200 or score >= 0:
            sub = display.subsurface(screenshot_rect)
            pygame.image.save(sub, "screenshot.png")
            score = evaluate_img(
                wallpaper,
                pygame.image.load(f"artworks{os.sep}to_scale{os.sep}{artwork}"),
            )
        else:
            score -= 1

        replay.render()

    pygame.display.flip()

    clock.tick()
