from cell import *
from colors import *
import pygame
import random

class Model:
    def __init__(self, cells_y, cells_x, width):
        self.win = pygame.display.set_mode((width, width))
        self.cells_y = cells_y       # nr of rows
        self.cells_x = cells_x       # nr of columns
        self.width = width           # display width
        self.gap = width // cells_y  # width of the spot

        Spot.set_parameters(cells_y, cells_x, self.gap, self.win)
        self.grid = [[Cell(j, i)
                      for i in range(cells_x)] for j in range(cells_y)]
        self.generate_random_forest()
    
    def generate_random_forest(self, trees=1900):
        random_list = random.sample(range(0, self.cells_y*self.cells_x - 1), trees)
        for nr in random_list:
            self.grid[nr//self.cells_x][nr%self.cells_x].make_tree()

    def draw(self):
        """Draws square grid with colored spots."""
        self.win.fill(Color.tea_green)
        for row in self.grid:
            for cell in row:
                cell.visual.draw()
        self.draw_grid()

    def draw_grid(self):
        """Draws square grid."""
        for row_idx in range(self.cells_y):
            pygame.draw.line(self.win, Color.dark_green,
                             (0, row_idx * self.gap), (self.width, row_idx*self.gap))
            for col_idx in range(self.cells_y):
                pygame.draw.line(self.win, Color.dark_green,
                                 (col_idx*self.gap, 0), (col_idx*self.gap, self.width))

    def get_clicked_pos(self, pos) -> tuple():
        """Returns row and columns idx of clicked place."""
        y, x = pos
        row = y // self.gap
        col = x // self.gap
        return row, col

    def make_spot_fire(self, row, col):
        self.grid[row][col].make_fire()

    def animate(self):
        pygame.display.set_caption("Fire figters vs fire")
        run = True
        while run:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed()[0]:  # LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)

                    # if pos is within the model.visual
                    if row < self.cells_y and col < self.cells_x:
                        self.make_spot_fire(row, col)

                # elif pygame.mouse.get_pressed()[2]:  # RIGHT
                #     pos = pygame.mouse.get_pos()
                #     row, col = model.visual.get_clicked_pos(pos)
                #     if row < width and col < width:
                #         model.visual.reset_spot(row, col)

                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE:
                #         model.visual.clear_old_grid()
                #         model.visual.update_cells()

                #     if event.key == pygame.K_c: # reset
                #         model.visual.reset()

            pygame.display.update()
        pygame.quit()
