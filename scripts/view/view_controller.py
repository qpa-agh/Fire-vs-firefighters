import pygame
from model.model import Model
from view.spot import Spot
from view.button_handler import ButtonHandler
from view.colors import Color


class ViewController:
    def __init__(self, width) -> None:
        self.win = pygame.display.set_mode((width + 100, width))
        pygame.display.set_caption("Fire figters vs fire")
        self.win.fill(Color.grass_green)
        
    def draw_model(self, model: Model):
        """Draws square grid with colored spots."""
        for row in model.grid:
            for cell in row:
                cell.visual.draw(self.win)
        
    def draw_buttons(self, button_handler: ButtonHandler):
        """Draws all buttons from list."""
        for button in button_handler.buttons:
            button.draw(self.win)

    def update(self):
        pygame.display.update()
        
    def get_clicked_pos(self, pos) -> tuple():
        """Returns row and columns idx of clicked place."""
        x, y = pos
        row = y // Spot.width
        col = x // Spot.width
        return row, col
