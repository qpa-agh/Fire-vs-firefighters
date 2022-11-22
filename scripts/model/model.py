from model.cell import *
from view.colors import *
from view.button import *
import random


class Model:
    def __init__(self, cells_y, cells_x, width):
        self.cells_y = cells_y       # nr of rows
        self.cells_x = cells_x       # nr of columns

        self.width = width           # display width
        self.gap = width // cells_y  # width of the spot
        Spot.set_parameters(self.gap)

        self.cells_on_fire = set()
        self.wind_direction = None # WindDirection 

        self.grid = [[Cell(j, i)
                      for i in range(cells_x)] for j in range(cells_y)]
        self.update_neigbours()
        self.generate_random_forest(20000)

    def generate_random_forest(self, trees=None):
        if not trees:
            trees = int(self.cells_y * self.cells_x * 0.8)
        random_list = random.sample(
            range(0, self.cells_y*self.cells_x - 1), trees)
        for nr in random_list:
            self.grid[nr//self.cells_x][nr %
                                        self.cells_x].wood = random.randint(1, 5)
            self.grid[nr//self.cells_x][nr % self.cells_x].make_tree()
        

    def make_spot_fire(self, row, col):
        if self.grid[row][col].cell_type == CellType.TREE:
            self.grid[row][col].make_fire()
            self.cells_on_fire.add(self.grid[row][col])

    def reset_spot(self, row, col):
        if self.grid[row][col].cell_type == CellType.FIRE:
            self.grid[row][col].make_tree()
            self.cells_on_fire.remove(self.grid[row][col])

    def reset_model(self):
        self.grid = [[Cell(j, i)
                      for i in range(self.cells_x)] for j in range(self.cells_y)]
        self.update_neigbours()
        self.generate_random_forest()

    def update_neigbours(self):
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                if row_idx > 0:
                    # left top corner
                    if col_idx > 0:
                        cell.neighbours[0] = self.grid[row_idx-1][col_idx-1]

                    # top
                    cell.neighbours[1] = self.grid[row_idx-1][col_idx]
                    
                    # right top corner
                    if col_idx < self.cells_x - 1:
                        cell.neighbours[2] = self.grid[row_idx-1][col_idx+1]

                # right
                if col_idx < self.cells_x - 1:
                    cell.neighbours[3] = self.grid[row_idx][col_idx+1]

                if row_idx < self.cells_y - 1:
                    # right bottom corner
                    if col_idx < self.cells_x - 1:
                        cell.neighbours[4] = self.grid[row_idx+1][col_idx+1]

                    # bottom
                    cell.neighbours[5] = self.grid[row_idx+1][col_idx]
                    
                    # left bottom corner
                    if col_idx > 0:
                        cell.neighbours[6] = self.grid[row_idx+1][col_idx-1]
                                # left
                if col_idx > 0:
                    cell.neighbours[7] = self.grid[row_idx][col_idx-1]

