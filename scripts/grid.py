from spot import Spot
from colors import Color
import pygame

class Grid:
    """Representation of squre grid on which visualisation happens."""
    def __init__(self, win, rows, width):
        self.grid = []
        self.win = win
        self.rows = rows
        self.cols = rows
        self.width = width
        gap = width // rows
        for row_idx in range(rows):
            self.grid.append([])
            for col_idx in range(rows):
                spot = Spot(row_idx, col_idx, gap, rows)
                self.grid[row_idx].append(spot)

    def get_grid(self):
        return self.grid

    def draw_grid(self):
        """Draws square grid."""
        gap = self.width // self.rows
        for row_idx in range(self.rows):
            pygame.draw.line(self.win, Color.dark_green, (0, row_idx*gap), (self.width, row_idx*gap))
            for col_idx in range(self.rows):
                pygame.draw.line(self.win, Color.dark_green, (col_idx*gap, 0), (col_idx*gap, self.width))
    
    def draw(self):
        """Draws square grid with colored spots."""
        self.win.fill(Color.tea_green)
        for row in self.grid:
            for spot in row:
                spot.draw(self.win)
        self.draw_grid()
    
    def draw_path(win, grid, rows, width):
        """Draws calculated path from start to end."""
        win.fill(Color.tea_green)
        for row in grid:
            for spot in row:
                spot.draw(win)
        Grid.draw_grid(win, rows, width)
        pygame.display.update()
    
    def clear_old_grid(win, grid, rows, width):
        """Erases all spots colored as an output of calculations."""
        win.fill(Color.tea_green)
        for row in grid:
            for spot in row:
                if spot.is_closed() or spot.is_open():
                    spot.reset()
                    spot.draw(win)
        Grid.draw_grid(win, rows, width)
        pygame.display.update()
    
    def get_clicked_pos(self, pos) -> tuple():
        """Returns row and columns idx of clicked place."""
        gap = self.width // self.rows
        y, x = pos

        row = y// gap
        col = x // gap
        return row, col
    
    def make_fire(self, row, col):
        self.grid[row][col].make_fire()

    def reset(self, row, col):
        self.grid[row][col].reset()
