from utils.enums import CellType, SectorType
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
        self.sector = -1

    def make_water(self):
        self.cell_type == CellType.WATER
        self.visual.make_water()

    def make_fire(self, spread_per_frame):
        self.cell_type = CellType.FIRE
        if self.wood > 0:
            self.wood -= spread_per_frame
            self.burning_wood +=  spread_per_frame
        self.visual.make_fire(self.wood, self.burning_wood, self.burned_wood)

    def make_tree(self):
        self.cell_type = CellType.TREE
        self.wood = random.randint(20, 99)
        self.visual.make_tree(self.wood)

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
