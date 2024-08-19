import pygame
import importlib
import sys

from widgets import Button, Label
import main

pygame.init()
(w, h) = (1000, 900)
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Drawn to scale")


def instructions():
    pygame.init()
    screen = pygame.display.set_mode((1000, 900))
    font = pygame.font.SysFont(None, 30)

    main_menu_button = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Menu", (183, 183, 183), 5, 5,
                              100, 50)
    inst = [
        Label(screen, pygame.font.SysFont(None, 100), "Instructions", (200, 100, 100), 450, 200, 100, 50),
        Label(screen, font, "Draw the following artwork.",
              (183, 183, 183), 450, 300, 100, 50),
        Label(screen, font, "You are a small player, whose vision is only limited.", (183, 183, 183), 450, 400, 100, 50),
        Label(screen, font, "You must draw to scale!", (183, 183, 183), 450, 450, 100, 50),
        Label(screen, font, "wasd to move", (183, 183, 183), 450, 500, 100, 50),
        Label(screen, font, "space to deploy paint", (183, 183, 183), 450, 550, 100, 50),
        Label(screen, font, "where you find the painting palette, press b to change buckets", (183, 183, 183), 450, 600, 100, 50),
    ]

    while True:
        event = pygame.event.wait()
        pos = pygame.mouse.get_pos()
        if main_menu_button.handle_event(event, pos):
            break
        if event.type == pygame.QUIT:
            break

        screen.fill((36, 34, 30))
        main_menu_button.render()
        for i in inst:
            i.render()
        pygame.display.update()


def options():
    pygame.init()
    screen = pygame.display.set_mode((1000, 900))
    font = pygame.font.SysFont(None, 30)

    main_menu_button = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Menu", (183, 183, 183), 5, 5,
                              100, 50)
    opts_l = [
        Label(screen, pygame.font.SysFont(None, 100), "Options", (200, 100, 100), 450, 200, 100, 50),
        Label(screen, font, "Background Music: ", (183, 183, 183), 450, 300, 100, 50),
        Label(screen, font, "SFX: ", (183, 183, 183), 450, 400, 100, 50),
    ]

    bgm_b = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "On", (183, 183, 183), 600, 300, 100, 50)
    sfx_b = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "On", (183, 183, 183), 600, 400, 100, 50)
    '''if not sfx.bgm_on:
        bgm_b.text = "Off"
    if not sfx.sfx_on:
        sfx_b.text = "Off"'''

    while True:
        event = pygame.event.wait()
        pos = pygame.mouse.get_pos()
        if main_menu_button.handle_event(event, pos):
            break
        if event.type == pygame.QUIT:
            break
        if bgm_b.handle_event(event, pos):
            if bgm_b.text == "On":
                bgm_b.text = "Off"
                main.sfxman.pause_music()
            elif bgm_b.text == "Off":
                bgm_b.text = "On"
                main.sfxman.start_music()
        if sfx_b.handle_event(event, pos):
            if sfx_b.text == "On":
                sfx_b.text = "Off"
            elif sfx_b.text == "Off":
                sfx_b.text = "On"

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
l = Label(screen, pygame.font.SysFont(None, 100), "Drawing to Scale", (200, 100, 100), 450, 150, 100, 50)
l2 = Label(screen, font, "GMTK 2024 Game Jam", (183, 183, 183), 450, 225, 100, 50)
b = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Play", (183, 183, 183), 200, 300, 600, 50)
i = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Instructions", (183, 183, 183), 200, 400, 600, 50)
o = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Options", (183, 183, 183), 200, 500, 600, 50)
q = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Quit", (183, 183, 183), 200, 600, 600, 50)
r = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Replay", (183, 183, 183), 200, 700, 600, 50)

while True:
    dt = clock.tick(60)
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if r.handle_event(event, pos):
            importlib.reload(main)
            ret = main.play()
            if ret == 1:
                b.text = "Resume"
            elif ret == 100:
                l2.text = "Congrats!! You Won!!"
        if b.handle_event(event, pos):
            ret = main.play()
            if ret == 1:
                b.text = "Resume"
            elif ret == 100:
                l2.text = "Congrats!! You Won!!"
        if q.handle_event(event, pos):
            pygame.quit()
            sys.exit(0)
        if i.handle_event(event, pos):
            instructions()
        if o.handle_event(event, pos):
            options()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    screen.fill((36, 34, 30))
    l.render()
    l2.render()
    b.render()
    i.render()
    o.render()
    q.render()
    r.render()
    pygame.display.update()
