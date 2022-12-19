from utils.enums import CellType, SectorType, TreeType
from view.spot import Spot
import random


class Cell:
    def __init__(self, row: int, col: int, cell_type: CellType = CellType.GROUND):
        self.cell_type = cell_type
        self.row = row
        self.col = col
        self.visual = Spot(row, col)
        self.neighbours = {}  # neighbor idx to cell
        self.wood = 0  # if tree -> random from 20 to 100
        self.burning_wood = 0
        self.burned_wood = 0
        self.sector = None
        self.moisture = 0 # from 0 to 1

    def make_water(self):
        self.cell_type == CellType.WATER
        self.visual.make_water()
    
    def evaporate(self, water_evaporation_per_frame: float):
        water = self.moisture * self.wood
        water -= water_evaporation_per_frame
        self.moisture = water/ self.wood

    def make_fire(self, spread_per_frame: float):
        self.cell_type = CellType.FIRE
        if self.wood > 0:
            self.wood -= spread_per_frame
            self.burning_wood +=  spread_per_frame
        self.visual.make_fire(self.wood, self.burning_wood, self.burned_wood)

    def make_tree(self, tree_factor: float, tree_type: TreeType):
        self.cell_type = CellType.TREE
        self.moisture = 0.6 if tree_type == TreeType.DECIDUOUS else 0.4
        self.wood = random.randint(10, 25) * tree_factor
        self.visual.make_tree(self.wood, tree_type)

    def make_burned(self):
        self.cell_type == CellType.BURNED
        self.visual.make_burned(self.burned_wood)

    def has_wood_to_burn(self) -> bool:
        return self.wood + self.burning_wood > 0

    def burn_wood(self, wood_to_burn: float, spread_per_frame: float) -> None:
        self.burning_wood -= wood_to_burn
        self.burned_wood += wood_to_burn
        if self.wood + self.burning_wood <= 0:
            self.make_burned()
        else:
            self.make_fire(spread_per_frame)

    def is_on_fire(self):
        return self.cell_type == CellType.FIRE

    def is_tree(self):
        return self.cell_type == CellType.TREE
