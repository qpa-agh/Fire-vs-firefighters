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
        self.view_type = ViewType.CELL

    def draw_model(self, model: Model):
        """Draws square grid with colored spots."""
        for row in model.grid:
            for cell in row:
                cell.visual.draw(self.view_type, cell.sector)
                
        self.draw_compass()

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

    def update(self):
        pygame.display.update()

    def get_clicked_pos(self, pos) -> tuple():
        """Returns row and columns idx of clicked place."""
        x, y = pos
        row = y // Spot.width
        col = x // Spot.width
        return row, col
