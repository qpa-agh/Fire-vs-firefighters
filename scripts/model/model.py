from model.cell import Cell
from model.fighter import Fighter, FighterAction
from model.team import Team
from solver.commander_actions import CommanderLogisticActionFactory
from utils.enums import Direction, SectorType, TreeType
from view.colors import *
from view.button import *
import random
import cv2


class Model:
    def __init__(self, cells_y, cells_x, gap, forest_map=None):
        assert cells_y % 10 == 0
        assert cells_x % 10 == 0
        self.cells_y = cells_y       # nr of rows
        self.cells_x = cells_x       # nr of columns

        self.sectors_y = cells_y // 10
        self.sectors_x = cells_x // 10

        View.gap = gap  # width of the spot
        View.width = gap * self.cells_x
        View.height = gap * self.cells_y

        self.cells_on_fire = set()
        self.wind_direction = None  # WindDirection

        self.grid = [[Cell(j, i)
                      for i in range(cells_x)] for j in range(cells_y)]
        self.update_neigbours()
        self.sectors = []

        self.sectors_with_fire = []
        self.flammable_sectors = []

        # how huge impact has amount of burning wood on fire spread
        self.tree_factor = 4

        # how much wood which is on fire will burn out per frame
        self.wood_burned_per_frame = 0.05

        # how much wood will catch fire per frame
        self.burning_spread_per_frame = 0.25

        # how much water evaporates from wood per frame
        self.water_evaporation_per_frame = 5

        self.start_x = 0 # start on the image x - img can be bigger
        self.start_y = 0
        self.zoom = 1

        if forest_map:
            self.load_sectors_from_img(forest_map)
        else:
            self.generate_random_forest()

        self.teams: list[Team] = []
        self.generate_fighters(10, [(15, 15), (16, 16), (17, 17)])

    def generate_fighters(self, per_sector, sectors):
        for sector in sectors:
            fighters = []
            for i in range(per_sector):
                fighters.append(self.__create_random_fighter(sector))
            self.teams.append(Team(fighters, sector))

    def load_sectors_from_img(self, forest_map):
        I = cv2.imread(forest_map, cv2.COLOR_BGR2RGB)  # blue - green -red
        if self.cells_x > I.shape[1] or self.cells_x > I.shape[1]:
            raise ValueError("Image is too small")
        if self.start_x + self.cells_x >= I.shape[1]:
            self.start_x = I.shape[1] - self.cells_x
        if self.start_y + self.cells_y >= I.shape[0]:
            self.start_y = I.shape[0] - self.cells_y

                
        sectors_flammable_cells = {}
        for sector_row in range(self.sectors_y):
            for sector_col in range(self.sectors_x):
                sectors_flammable_cells[(sector_row, sector_col)] = 0

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                sector = (y // 10, x // 10)
                img_cell = I[y+self.start_y][x+self.start_x]
                if img_cell[0] >= 200: # blue
                    cell.make_water()
                elif img_cell[1] < 100 and img_cell[1] > 90 and img_cell[0] < 10 and img_cell[2] < 10:  # green
                    cell.make_tree(self.tree_factor, TreeType.CONIFEROUS)
                    sectors_flammable_cells[sector] += 1
                elif img_cell[1] > 150 and img_cell[0] < 40 and img_cell[2] < 40:  # leafy
                    cell.make_tree(self.tree_factor, TreeType.DECIDUOUS)
                    sectors_flammable_cells[sector] += 1
                elif random.random() <= 0.8:
                    cell.make_grass()

        for sector_row in range(self.sectors_y):
            for sector_col in range(self.sectors_x):
                sector = (sector_row, sector_col)
                if sectors_flammable_cells[sector] >= 30:
                    self.flammable_sectors.append(sector)


    def generate_sectors(self):
        trees_ratio = 0.8
        grass_ratio = 0.1
        for sector_y in range(self.sectors_y):
            for sector_x in range(self.sectors_x):
                rand = random.random()
                sector = None
                if rand < trees_ratio:
                    sector = SectorType.TREES
                    self.flammable_sectors.append((sector_y, sector_x))
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
                        or (cell.sector == SectorType.GRASS and random.random() <= 0.2):
                    cell.make_tree(self.tree_factor, TreeType.DECIDUOUS)
                elif cell.sector == SectorType.WATER:
                    cell.make_water()

    def make_spot_fire(self, row, col):
        if self.grid[row][col].is_tree():
            self.grid[row][col].make_fire(self.burning_spread_per_frame)
            self.cells_on_fire.add(self.grid[row][col])
            sector = (row // 10, col // 10)
            if sector not in self.sectors_with_fire:
                self.sectors_with_fire.append(sector)
                if sector in self.flammable_sectors:
                    self.flammable_sectors.remove(sector)

    def reset_spot(self, row, col):
        if self.grid[row][col].is_on_fire():
            self.grid[row][col].make_tree(self.tree_factor, TreeType.DECIDUOUS)
            self.cells_on_fire.remove(self.grid[row][col])

    def reset_model(self):
        self.grid = [[Cell(j, i)
                      for i in range(self.cells_x)] for j in range(self.cells_y)]
        self.update_neigbours()
        self.generate_random_forest()
        self.teams = []
        self.generate_fighters(5, [(15, 15), (16, 16), (17, 17), (14, 16), (13, 17), 
                            (17, 19), (17, 20), (16, 21), (15, 19), (15, 20), (14, 21), (13, 20), (13, 19)])

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

    def __create_random_fighter(self, sector):
        min_y, max_y, min_x, max_x = self.__get_sector_bounds(sector)
        y = random.randrange(min_y, max_y)
        x = random.randrange(min_x, max_x)
        action = FighterAction.random_action()
        direction = Direction.random_direction()
        return Fighter(y, x, (min_y, max_y, min_x, max_x), action, direction)

    def __get_sector_bounds(self, sector):
        return sector[0] * 10, (sector[0] + 1) * 10, sector[1] * 10, (sector[1] + 1) * 10 

    def apply_actions(self, actions):
        factory = CommanderLogisticActionFactory()
        for action in actions:
            working_action = factory.create_action(action)
            working_action.run_action(self)

    def update_sector_on_fire(self, sector):
        bounds = self.__get_sector_bounds(sector)
        on_fire = False
        for y, row in enumerate(self.grid[bounds[0]: bounds[1]]):
            if on_fire:
                break
            for x, cell in enumerate(row[bounds[2]: bounds[3]]):
                if cell.is_on_fire():
                    on_fire = True
                    break
        
        if on_fire and sector not in self.sectors_with_fire:
            self.sectors_with_fire.append(sector)
            if sector in self.flammable_sectors:
                self.flammable_sectors.remove(sector)
        if not on_fire and sector in self.sectors_with_fire:
            self.sectors_with_fire.remove(sector)
            if sector not in self.flammable_sectors:
                self.flammable_sectors.append(sector)
