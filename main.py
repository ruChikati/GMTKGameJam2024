import os
import sys
import time

import pygame

import input
from anim import Animation
from entity import Entity
from wallpaper import Wallpaper
from sound import SFXManager
from widgets import Button

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
floor_surf = pygame.image.load(f".{os.sep}tiles{os.sep}brick.png")
colours = ["blue", "black", "brick", "cyan", "green", "magenta", "red", "white", "yellow"]
imgb = None
for i in range(16):
    floor_tiles.append((pygame.Vector2(-256 + 32 * i, 0), floor_surf))
    if 12 > i >= 2:
        imgb = pygame.image.load(f".{os.sep}tiles{os.sep}{colours[i % len(colours)]}.png")
    else:
        imgb = floor_surf
    floor_tiles.append((pygame.Vector2(-256 + 32 * i, 32), imgb))
    floor_tiles.append((pygame.Vector2(-256 + 32 * i, 64), floor_surf))

sfxman = SFXManager()
sfxman.adjust_volume("paint", 0.1)
sfxman.add_queue(
    f".{os.sep}sounds{os.sep}sfx{os.sep}music{os.sep}" + os.listdir(f".{os.sep}sounds{os.sep}sfx{os.sep}music{os.sep}")[
        0])
sfxman.adjust_bgm_volume(0.1)
sfxman.start_music()



def play():
    global last_time, dt, display, screen

    pos_i = 0

    scroll = pygame.Vector2(-152, -119)
    zoom = pygame.Vector2(1, 1)

    display = pygame.display.set_mode((1280, 720))

    font = pygame.font.SysFont(None, 30)
    main_menu_button = Button(display, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Menu", (183, 183, 183),
                              0 - scroll.x, 0 + scroll.y,
                              100, 50) # FIXME not rendering

    running = True
    while running:

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
            mpos = pygame.mouse.get_pos()
            if main_menu_button.handle_event(event, mpos):
                running = False
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
                case input.KEYDOWN:
                    match event.key:
                        case input.B:
                            if player.rect.y >= 0 and -160 <= player.rect.x <= 96:
                                sfxman.play("bucket")
                                print(player.rect.x, end=",")
                                pos_i = (player.rect.x // 32) - 1
                                print(pos_i)
                        case input.SPACE:
                            if player.rect.y <= 0:
                                sfxman.play("paint", 2)
                                for i in range(16):
                                    for j in range(16):
                                        try:
                                            if player.rect.colliderect(wallpaper.w_tiles[i][j].rect):
                                                wallpaper.w_tiles[i][j].change_status(colours[pos_i % len(colours)])
                                                break
                                        except IndexError:
                                            pass
                case input.MOUSEWHEEL:
                    zoom += pygame.Vector2(event.y, event.y) * 0.01

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
            screen.blit(pos[1], pos[0] - scroll)
        wallpaper.draw(scroll)
        player.update(dt, scroll)
        main_menu_button.render() # FIXME not rendering

        display.blit(pygame.transform.scale(screen, (zoom.x * display.get_width(), zoom.y * display.get_height())), (0, 0))
        pygame.display.flip()
        clock.tick()

if __name__ == '__main__':
    import start