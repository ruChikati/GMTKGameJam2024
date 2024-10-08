import pygame
import input


class Button:
    def __init__(
        self,
        surface: pygame.Surface,
        colour: tuple[int, int, int],
        hover_colour: tuple[int, int, int],
        click_colour: tuple[int, int, int],
        font: pygame.font.SysFont,
        text: str,
        text_colour: tuple[int, int, int],
        x: int,
        y: int,
        w: int,
        h: int,
    ):
        self.surface = surface
        self.colour = colour
        self.hover_colour = hover_colour
        self.click_colour = click_colour
        self.render_colour = colour
        self.font = font
        self.text = text
        self.text_colour = text_colour
        self.rect = pygame.Rect(x, y, w, h)

        self.clicked = False

    def handle_event(
        self, event: pygame.event, mousepos: pygame.Vector2 | tuple[int, int], event_handled: bool = False
    ) -> bool:
        if self.rect.collidepoint(mousepos):
            self.render_colour = self.hover_colour
        else:
            self.render_colour = self.colour
        if not event_handled:
            if event.type == pygame.MOUSEBUTTONUP or event.type == input.MOUSEUP:
                if self.rect.collidepoint(mousepos):
                    self.clicked = True
                    return True
        else:
            if self.rect.collidepoint(mousepos):
                self.clicked = True
                return True

        self.clicked = False
        return False

    def render(self):
        if self.clicked:
            self.render_colour = self.click_colour

        pygame.draw.rect(self.surface, self.render_colour, self.rect)
        size = self.font.size(self.text)
        self.surface.blit(
            self.font.render(self.text, True, self.text_colour),
            (
                self.rect.x + (self.rect.width / 2) - (size[0] / 2),
                self.rect.y + (self.rect.height / 2) - (size[1] / 2),
            ),
        )


class Label:
    def __init__(
        self,
        surface: pygame.Surface,
        font: pygame.font.SysFont,
        text: str,
        colour: tuple[int, int, int],
        x: int,
        y: int,
        w: int,
        h: int,
    ):
        self.surface = surface
        self.font = font
        self.text = text
        self.colour = colour
        self.rect = pygame.Rect(x, y, w, h)

    def render(self):
        size = self.font.size(self.text)
        self.surface.blit(
            self.font.render(self.text, True, self.colour),
            (
                self.rect.x + (self.rect.width / 2) - (size[0] / 2),
                self.rect.y + (self.rect.height / 2) - (size[1] / 2),
            ),
        )
