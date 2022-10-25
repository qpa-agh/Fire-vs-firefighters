from spot import Spot
from colors import Color
import pygame

class Grid:
    """Representation of squre grid on which visualisation happens."""

    def make_grid(rows, width) -> list(list()):
        """Returns the grid initialised with spot objects."""
        grid = []
        gap = width // rows
        for row_idx in range(rows):
            grid.append([])
            for col_idx in range(rows):
                spot = Spot(row_idx, col_idx, gap, rows)
                grid[row_idx].append(spot)
        return grid

    def draw_grid(win, rows, width):
        """Draws square grid."""
        gap = width // rows
        for row_idx in range(rows):
            pygame.draw.line(win, Color.dark_green, (0, row_idx*gap), (width, row_idx*gap))
            for col_idx in range(rows):
                pygame.draw.line(win, Color.dark_green, (col_idx*gap, 0), (col_idx*gap, width))
    
    def draw(win, grid, rows, width):
        """Draws square grid with colored spots."""
        win.fill(Color.tea_green)
        for row in grid:
            for spot in row:
                spot.draw(win)
        Grid.draw_grid(win, rows, width)
    
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
                if spot.is_closed() or spot.is_open() or spot.is_path():
                    spot.reset()
                    spot.draw(win)
        Grid.draw_grid(win, rows, width)
        pygame.display.update()
    
    def get_clicked_pos(pos, rows, width) -> tuple():
        """Returns row and columns idx of clicked place."""
        gap = width // rows
        y, x = pos

        row = y// gap
        col = x // gap
        return row, col
