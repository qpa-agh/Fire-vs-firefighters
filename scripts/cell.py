from spot import Spot
from enum import Enum


class CellType(Enum):
    GROUND = 0,
    TREE = 1,
    FIRE = 2,
    BURNED = 3,
    GRASS = 4


class Cell:
    def __init__(self, row: int, col: int, cell_type: CellType=CellType.GROUND):
        self.cell_type = cell_type
        self.row = row
        self.col = col
        self.visual = Spot(row, col)
        self.neighbours = []
    
    def make_fire(self):
        self.cell_type = CellType.FIRE
        self.visual.make_fire() 
    
    def make_tree(self):
        self.cell_type = CellType.TREE
        self.visual.make_tree() 