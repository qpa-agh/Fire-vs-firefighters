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
    
    def is_closed(self):
        """Return if the spot was visited and is closed for searches."""
        return self.color == Color.dark_red
    
    def is_open(self):
        """Return if the spot was visited and is open for searches."""
        return self.color == Color.red
    
    def is_barrier(self):
        """Return if the spot is part of the barrier."""
        return self.color == Color.black
    
    def is_start(self):
        """Return if the spot is the start point."""
        return self.color == Color.auburn
    
    def reset(self):
        """Reset the color of the spot to default one."""
        self.color = Color.tea_green
    
    def make_closed(self):
        """Set the spot as visited and closed for search point by proper coloring."""
        self.color = Color.dark_red
    
    def make_open(self):
        """Set the spot as a part of a visited points area by proper coloring."""
        self.color = Color.red
    
    def make_barrier(self):
        """Set the spot as a part of a barrier by proper coloring."""
        self.color = Color.black
    
    def make_start(self):
        """Sets the spot as the start point by proper coloring."""
        self.color = Color.auburn
    
    def draw(self, win):
        """Draw the square with proper color and standaralized size."""
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbours(self, grid):
        """Updates neighbours list with all spot's neighbours."""
        self.neighbours = []

        # down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): 
            self.neighbours.append(grid[self.row + 1][self.col])

        # up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): 
            self.neighbours.append(grid[self.row - 1][self.col])

        # left
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): 
            self.neighbours.append(grid[self.row][self.col+1])

        # right
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): 
            self.neighbours.append(grid[self.row][self.col-1])
    
    def get_neighbours(self):
        return self.neighbours
