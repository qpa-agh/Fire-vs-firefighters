from model.cell import *
from view.colors import *
from view.button import *
import random


class Model:
    def __init__(self, cells_y, cells_x, width):
        assert cells_y % 10 == 0
        assert cells_x % 10 == 0
        self.cells_y = cells_y       # nr of rows
        self.cells_x = cells_x       # nr of columns

        self.sectors_y = cells_y // 10
        self.sectors_x = cells_x // 10

        self.width = width           # display width
        self.gap = width // cells_y  # width of the spot
        Spot.set_width(self.gap)

        self.cells_on_fire = set()
        self.wind_direction = None  # WindDirection

        self.grid = [[Cell(j, i)
                      for i in range(cells_x)] for j in range(cells_y)]
        self.update_neigbours()
        self.sectors = []
        self.generate_random_forest()

    def generate_random_forest(self): # TODO sectors from argument
        tree_sectors = int(self.sectors_y * self.sectors_x * 0.8)
        random_list = random.sample(
            range(self.sectors_y * self.sectors_x - 1), tree_sectors)
        for sector_y in range(self.sectors_y):
            row = []
            for sector_x in range(self.sectors_x):
                sector = sector_y * self.sectors_x + sector_x
                if sector in random_list:
                    row.append(SectorType.TREES)
                else:
                    row.append(SectorType.GRASS)
            self.sectors.append(row)

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                sectorTree = (y//10 * self.sectors_x + x//10) in random_list
                cell.sector = SectorType.TREES if sectorTree else SectorType.GRASS
                isTree = random.random() <= (0.7 if sectorTree else 0.2)
                if isTree:
                    cell.wood = random.randint(20, 99)
                    cell.make_tree()


    def make_spot_fire(self, row, col):
        if self.grid[row][col].is_tree():
            self.grid[row][col].make_fire()
            self.cells_on_fire.add(self.grid[row][col])

    def reset_spot(self, row, col):
        if self.grid[row][col].is_on_fire():
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
