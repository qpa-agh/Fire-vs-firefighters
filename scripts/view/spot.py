from view.colors import Color
import pygame


class Spot:
    """Representation of the pixel on a grid."""
    width = None  # spots width = gap between 2 lines
    window = None

    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.x = row * Spot.width
        self.y = col * Spot.width
        self.color = Color.ground
        self.neighbours = []

    def get_pos(self):
        """Returns idx of row and column of the object."""
        return self.row, self.col

    def draw(self):
        """Draw the square with proper color and standaralized size."""
        pygame.draw.rect(
            Spot.window, self.color, (self.y, self.x, Spot.width, Spot.width))

    def make_fire(self, wood, burned_wood):
        stage = burned_wood/(burned_wood + wood) * 6
        self.color = Color.fire[int(stage)]

    def make_burned(self, burned_wood: int):
        if burned_wood >= 1:
            burned_wood -= 1
        else:
            burned_wood = 0
        self.color = Color.burned[int(burned_wood)]

    def make_tree(self, wood: int):
        self.color = Color.tree[wood-1]

    @staticmethod
    def set_width(width):
        """Sets global parameters for all dots."""
        Spot.width = width

    @staticmethod
    def set_window(window):
        """Sets global parameters for all dots."""
        Spot.window = window
