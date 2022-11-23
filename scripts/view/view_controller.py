import pygame
from model.model import Model
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

    def draw_model(self, model: Model):
        """Draws square grid with colored spots."""
        for row in model.grid:
            for cell in row:
                cell.visual.draw()
        self.display_compass()

    def draw_buttons(self, button_handler: ButtonHandler):
        """Draws all buttons from list."""
        for button in button_handler.buttons:
            button.draw()
        self.display_compass()
        # self.display_directions()

    def update(self):
        pygame.display.update()

    def get_clicked_pos(self, pos) -> tuple():
        """Returns row and columns idx of clicked place."""
        x, y = pos
        row = y // Spot.width
        col = x // Spot.width
        return row, col
    
    def display_compass(self):
        imp = pygame.image.load("scripts\img\compass_small.png").convert_alpha()
        self.win.blit(imp, (self.width + 25, self.width - 190))
    
    def display_directions(self):
        smallfont = pygame.font.SysFont('Verdana', 17)
        labels_to_pos = {
            "N": (self.width + 94,self.width - 215),
            "S": (self.width + 94,self.width - 35),
            "W": (self.width + 5,self.width - 125),
            "E": (self.width + 180,self.width - 125),
            "NW": (self.width + 25,self.width - 190),
            "NE": (self.width + 145,self.width - 190),
            "SE": (self.width + 145,self.width - 60),
            "SW": (self.width + 25,self.width - 60),
        }
        for label, pos in labels_to_pos.items():
            text = smallfont.render(label, True, Color.black)
            self.win.blit(text, pos)
