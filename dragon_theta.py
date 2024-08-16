import sys

import pygame

import theta

pygame.display.init()

theta.set_default_data_path()
game = theta.Game(pygame.display.Info().current_w, pygame.display.Info().current_h, 120)

game.set_name("The Dragon")
game.set_icon("./data/icon.png")
game.camera.set_background((220, 120, 62))

# TODO: work on `Modifier` class for anims (change colour based on hp)

gravity = pygame.Vector2(0, 0)

player = game.world.current_lvl.entities[0]
dragon = game.world.current_lvl.entities[1]

while True:

    player.accelerate(gravity)
    dragon.accelerate(gravity)

    for event in game.input.get():
        match event.type:
            case theta.input.QUIT:
                pygame.quit()
                sys.exit()
            case theta.input.KEYDOWN2:
                match event.key:
                    case theta.input.ESCAPE:
                        pygame.quit()
                        sys.exit()
            case theta.input.KEYHOLD:
                match event.key:
                    case theta.input.W | theta.input.SPACE:
                        player.accelerate(pygame.Vector2(0, -1))
                    case theta.input.A:
                        player.accelerate(pygame.Vector2(-1, 0))
                    case theta.input.S:
                        player.accelerate(pygame.Vector2(0, 1))
                    case theta.input.D:
                        player.accelerate(pygame.Vector2(1, 0))

    game.update()
