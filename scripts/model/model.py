from model.cell import *
from view.colors import *
from view.button import *
import random
import cv2


class Model:
    def __init__(self, cells_y, cells_x, width, forest_map=None):
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

        if forest_map:
            self.load_sectors_from_img()
        else:
            self.generate_random_forest()
        

        self.tree_factor = 4
        self.wood_burned_per_frame = 0.05
        self.burning_spread_per_frame = 0.25
        self.water_evaporation_per_frame = 0.01
    
    def load_sectors_from_img(self):
        I = cv2.imread('maps\map1.png', cv2.IMREAD_GRAYSCALE)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if I[y][x] == 255:
                    cell.make_water()
                elif I[y][x] > 200:
                    if random.random() <= 0.1:
                        cell.make_tree(4) #  self.tree_factor didn't work wtf
                elif random.random() <= 0.7:
                    cell.make_tree(4) #  self.tree_factor didn't work wtf
    
    def generate_sectors(self):
        trees_ratio = 0.8
        grass_ratio = 0.1
        for sector_y in range(self.sectors_y):
            for sector_x in range(self.sectors_x):
                rand = random.random()
                sector = None
                if rand < trees_ratio:
                    sector = SectorType.TREES
                elif rand < trees_ratio + grass_ratio:
                    sector = SectorType.GRASS
                else:
                    sector = SectorType.WATER
                self.sectors.append(sector)

    def generate_random_forest(self):
        self.generate_sectors()
        
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                sector_idx = (y//10 * self.sectors_x + x//10)
                cell.sector = self.sectors[sector_idx]
                if (cell.sector == SectorType.TREES and random.random() <= 0.7) \
                    or (cell.sector == SectorType.GRASS and random.random() <= 0.2) :
                    cell.make_tree(4) #  self.tree_factor didn't work wtf
                elif cell.sector == SectorType.WATER:
                    cell.make_water()

    def make_spot_fire(self, row, col):
        if self.grid[row][col].is_tree():
            self.grid[row][col].make_fire(self.burning_spread_per_frame)
            self.cells_on_fire.add(self.grid[row][col])

    def reset_spot(self, row, col):
        if self.grid[row][col].is_on_fire():
            self.grid[row][col].make_tree(self.tree_factor)
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
