from view.spot import Spot
from enum import Enum


class CellType(Enum):
    GROUND = 0,
    TREE = 1,
    FIRE = 2,
    BURNED = 3,
    GRASS = 4


class Cell:
    def __init__(self, row: int, col: int, cell_type: CellType = CellType.GROUND):
        self.cell_type = cell_type
        self.row = row
        self.col = col
        self.visual = Spot(row, col)
        self.neighbours = {}  # neighbor idx to cell
        self.wood = 0  # if tree -> random from 1 to 5
        self.burned_wood = 0

    def make_fire(self):
        self.cell_type = CellType.FIRE
        self.visual.make_fire(self.wood, self.burned_wood)

    def make_tree(self):
        self.cell_type = CellType.TREE
        self.visual.make_tree(self.wood)

    def make_burned(self):
        self.cell_type == CellType.BURNED
        self.visual.make_burned(self.burned_wood)
