from colors import Color
import pygame


class Spot:
    """Representation of the pixel on a grid."""
    total_rows = None
    total_cols = None
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

    def is_fire(self):
        return self.color == Color.fire
    
    def make_tree(self):
        self.color = Color.tree

    def update_neighbours(self, grid):
        """Updates neighbours list with all spot's neighbours."""
        self.neighbours = []

        # down
        if self.row < Spot.total_rows - 1: 
            self.neighbours.append(grid[self.row + 1][self.col])

        # up
        if self.row > 0: 
            self.neighbours.append(grid[self.row - 1][self.col])

        # left
        if self.col < Spot.total_rows - 1: 
            self.neighbours.append(grid[self.row][self.col+1])

        # right
        if self.col > 0: 
            self.neighbours.append(grid[self.row][self.col-1])
    
    @staticmethod
    def set_parameters(total_rows_, total_cols_, width_, win):
        Spot.total_rows = total_rows_
        Spot.total_cols = total_cols_
        Spot.width = width_
        Spot.win = win