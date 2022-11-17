from spot import Spot
from enum import Enum


class CellType(Enum):
    GROUND = 0,
    TREE = 1,
    FIRE = 2,
    BURNED = 3,
    GRASS = 4


class Cell:
    def __init__(self, cell_type: CellType, row: int, col: int):
        self.cell_type = cell_type
        self.row = row
        self.col = col
        self.visual = Spot(row, col)
        self.neighbours = []