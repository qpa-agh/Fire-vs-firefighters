from enum import Enum
import pygame
from model.model import Model
from utils.enums import ViewType
from view.button import Button
from view.spot import Spot
from view.button_handler import ButtonHandler
from view.colors import Color


class ViewController:
    def __init__(self, width) -> None:
        self.width = width
        self.win = pygame.display.set_mode((width + 200, width))
        Spot.set_window(self.win)
        Button.set_window(self.win)
        pygame.display.set_caption("Fire figters vs fire")
        self.win.fill(Color.white)
        self.view_type = ViewType.MAP

    def draw_model(self, model: Model, iteration):
        """Draws square grid with colored spots."""
        for row in model.grid:
            for cell in row:
                cell.visual.draw()

        if self.view_type == ViewType.FIRE_FIGHTERS:
            self.draw_fog()
            for team in model.teams:
                self.draw_fighters(team.fighters)

        self.draw_compass()
        self.draw_time(iteration)

    def draw_fighters(self, fighters):
        for fighter in fighters:
            fighter.draw(Spot.window, Spot.width, Spot.width)

    def draw_fog(self):
        """Add a layer of gray fog to enable fire figthers more cleaner visualization."""
        shape_surf = pygame.Surface(pygame.Rect(
            (0, 0, self.width, self.width)).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, Color.fog, shape_surf.get_rect())
        Spot.window.blit(shape_surf, (0, 0, self.width, self.width))

    def draw_buttons(self, button_handler: ButtonHandler):
        """Draws all buttons from list."""
        for button in button_handler.buttons:
            button.draw()
        self.draw_compass()

    def draw_compass(self):
        """Draws compass image."""
        imp = pygame.image.load(
            "scripts\img\compass_small.png").convert_alpha()
        self.win.blit(imp, (self.width + 25, self.width - 190))

    def draw_time(self, iteration):
        pygame.draw.rect(Button.window, Color.white, [
            self.width + 25, self.width - 300, 180, 20])
        smallfont = pygame.font.SysFont('Verdana', 16)
        text = smallfont.render("Time: " + "{:.2f}".format(iteration / 15) + " min", True, Color.black)  # 360 it -> 12 min
        Button.window.blit(text, (self.width + 25, self.width - 300))

    def update(self):
        pygame.display.update()

    def get_clicked_pos(self, pos) -> tuple():
        """Returns row and columns idx of clicked place."""
        x, y = pos
        row = y // Spot.width
        col = x // Spot.width
        return row, col
