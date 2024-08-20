import os
import random
import sys

import pygame

from sound import SFXManager
from widgets import Button, Label

pygame.init()
(w, h) = (1000, 900)
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Drawn to scale")

sfxman = SFXManager()
sfxman.adjust_volume("paint", 0.1)
sfxman.adjust_volume("button", 0.1)
sfxman.add_queue(
    f".{os.sep}sounds{os.sep}sfx{os.sep}music{os.sep}"
    + os.listdir(f".{os.sep}sounds{os.sep}sfx{os.sep}music{os.sep}")[0]
)
sfxman.adjust_bgm_volume(0.1)
sfxman.start_music()

artwork = random.choice(os.listdir("artworks"))
artwork_surf = pygame.image.load(f"artworks{os.sep}{artwork}")
rect = artwork_surf.get_rect()
rect.w /= 5
rect.h /= 5
artwork_surf = pygame.transform.scale(artwork_surf, (rect.w, rect.h))

def instructions():
    pygame.init()
    display = pygame.display.set_mode((1000, 900))
    c_font = pygame.font.SysFont(None, 30)

    main_menu_button = Button(
        display,
        (180, 20, 10),
        (180, 80, 10),
        (10, 75, 20),
        c_font,
        "Menu",
        (183, 183, 183),
        5,
        5,
        100,
        50,
    )
    inst = [
        Label(
            display,
            pygame.font.SysFont(None, 100),
            "Instructions",
            (200, 100, 100),
            450,
            200,
            100,
            50,
        ),
        Label(
            display,
            c_font,
            "Draw the following artwork:",
            (183, 183, 183),
            450,
            300,
            100,
            50,
        ),
        Label(
            display,
            c_font,
            "You are a small player, whose vision is only limited.",
            (183, 183, 183),
            450,
            500,
            100,
            50,
        ),
        Label(
            display,
            c_font,
            "You must draw to scale!",
            (183, 183, 183),
            450,
            550,
            100,
            50,
        ),
        Label(display, c_font, "W-A-S-D to move", (183, 183, 183), 450, 600, 100, 50),
        Label(display, c_font, "Space to paint and 'r' to pick-up the ladder", (183, 183, 183), 450, 650, 100, 50),
        Label(
            display,
            c_font,
            "'e' to change paint colour, when directly on the paint",
            (183, 183, 183),
            450,
            700,
            100,
            50,
        ),
        Label(
            display,
            c_font,
            "'q' to toggle image",
            (183, 183, 183),
            450,
            750,
            100,
            50,
        ),
        Label(
            display,
            c_font,
            "When you are done, hit enter/return to see your artwork to compare with the final piece",
            (183, 183, 183),
            450,
            800,
            100,
            50,
        ),
    ]

    while True:
        event = pygame.event.wait()
        pos = pygame.mouse.get_pos()
        if main_menu_button.handle_event(event, pos):
            sfxman.play("button")
            break
        if event.type == pygame.QUIT:
            break

        display.fill((36, 34, 30))
        display.blit(artwork_surf, (450, 350))
        main_menu_button.render()
        for i in inst:
            i.render()
        pygame.display.update()


def options():
    pygame.init()
    screen = pygame.display.set_mode((1000, 900))
    font = pygame.font.SysFont(None, 30)

    main_menu_button = Button(
        screen,
        (180, 20, 10),
        (180, 80, 10),
        (10, 75, 20),
        font,
        "Menu",
        (183, 183, 183),
        5,
        5,
        100,
        50,
    )
    opts_l = [
        Label(
            screen,
            pygame.font.SysFont(None, 100),
            "Options",
            (200, 100, 100),
            450,
            200,
            100,
            50,
        ),
        Label(screen, font, "Background Music: ", (183, 183, 183), 450, 300, 100, 50),
        Label(screen, font, "SFX: ", (183, 183, 183), 450, 400, 100, 50),
    ]

    bgm_b = Button(
        screen,
        (180, 20, 10),
        (180, 80, 10),
        (10, 75, 20),
        font,
        "On",
        (183, 183, 183),
        600,
        300,
        100,
        50,
    )
    sfx_b = Button(
        screen,
        (180, 20, 10),
        (180, 80, 10),
        (10, 75, 20),
        font,
        "On",
        (183, 183, 183),
        600,
        400,
        100,
        50,
    )
    if sfxman.paused:
        bgm_b.text = "Off"
    if not sfxman.sfx_enabled:
        sfx_b.text = "Off"

    while True:
        event = pygame.event.wait()
        pos = pygame.mouse.get_pos()
        if main_menu_button.handle_event(event, pos):
            sfxman.adjust_volume("paint", 0.1)
            break
        if event.type == pygame.QUIT:
            break
        if bgm_b.handle_event(event, pos):
            if bgm_b.text == "On":
                bgm_b.text = "Off"
                sfxman.play("button")
                sfxman.pause_music()
            elif bgm_b.text == "Off":
                bgm_b.text = "On"
                sfxman.play("button")
                sfxman.unpause_music()
        if sfx_b.handle_event(event, pos):
            if sfx_b.text == "On":
                sfx_b.text = "Off"
                sfxman.play("button")
                sfxman.toggle_sound(False)
            elif sfx_b.text == "Off":
                sfx_b.text = "On"
                sfxman.play("button")
                sfxman.toggle_sound(True)

        screen.fill((36, 34, 30))
        main_menu_button.render()
        for i in opts_l:
            i.render()
        bgm_b.render()
        sfx_b.render()
        pygame.display.update()


try:
    # pygame-ce
    clock = pygame.Clock()
except AttributeError:
    # pygame
    clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)
l = Label(
    screen,
    pygame.font.SysFont(None, 100),
    "Drawing to Scale",
    (200, 100, 100),
    450,
    150,
    100,
    50,
)
l2 = Label(screen, font, "GMTK 2024 Game Jam", (183, 183, 183), 450, 225, 100, 50)
b = Button(
    screen,
    (180, 20, 10),
    (180, 80, 10),
    (10, 75, 20),
    font,
    "Play",
    (183, 183, 183),
    200,
    300,
    600,
    50,
)
i = Button(
    screen,
    (180, 20, 10),
    (180, 80, 10),
    (10, 75, 20),
    font,
    "Instructions",
    (183, 183, 183),
    200,
    400,
    600,
    50,
)
o = Button(
    screen,
    (180, 20, 10),
    (180, 80, 10),
    (10, 75, 20),
    font,
    "Options",
    (183, 183, 183),
    200,
    500,
    600,
    50,
)
q = Button(
    screen,
    (180, 20, 10),
    (180, 80, 10),
    (10, 75, 20),
    font,
    "Quit",
    (183, 183, 183),
    200,
    600,
    600,
    50,
)


def start():
    global screen
    while True:
        dt = clock.tick(60)
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if b.handle_event(event, pos):
                screen = pygame.display.set_mode((w, h))
                sfxman.play("button")
                return 1
            if q.handle_event(event, pos):
                sfxman.play("button")
                pygame.quit()
                sys.exit(0)
            if i.handle_event(event, pos):
                sfxman.play("button")
                instructions()
            if o.handle_event(event, pos):
                sfxman.play("button")
                options()
            if event.type == pygame.QUIT:
                sfxman.play("button")
                pygame.quit()
                sys.exit(0)

        screen.fill((36, 34, 30))
        l.render()
        l2.render()
        b.render()
        i.render()
        o.render()
        q.render()
        pygame.display.update()
