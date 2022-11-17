from colors import Color
import pygame


class Spot:
    """Representation of the pixel on a grid."""

    def __init__(self, row, col, width, total_rows) -> None:
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = Color.tea_green
        self.neighbours = []

    def get_pos(self):
        """Returns idx of row and column of the object."""
        return self.row, self.col

    def draw(self, win):
        """Draw the square with proper color and standaralized size."""
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def make_fire(self):
        """Sets the spot as the start point by proper coloring."""
        self.color = Color.fire

    def is_fire(self):
        """Return if the spot is the start point."""
        return self.color == Color.fire

    def reset(self):
        """Reset the color of the spot to default one."""
        self.color = Color.tea_green
