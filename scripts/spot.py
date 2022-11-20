from colors import Color
import pygame


class Spot:
    """Representation of the pixel on a grid."""
    width = None # spots width = gap between 2 lines
    win = None

    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.x = row * Spot.width
        self.y = col * Spot.width
        self.color = Color.tea_green
        self.neighbours = []

    def get_pos(self):
        """Returns idx of row and column of the object."""
        return self.row, self.col

    def draw(self):
        """Draw the square with proper color and standaralized size."""
        pygame.draw.rect(
            Spot.win, self.color, (self.x, self.y, Spot.width, Spot.width))

    def make_fire(self):
        self.color = Color.fire

    def make_burned(self):
        self.color = Color.burned
    
    def make_tree(self):
        self.color = Color.tree
    
    @staticmethod
    def set_parameters(width_, win):
        """Sets global parameters for all dots."""
        Spot.width = width_
        Spot.win = win