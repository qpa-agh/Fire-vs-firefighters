from utils.enums import CellType, SectorType
from view.spot import Spot

class Cell:
    def __init__(self, row: int, col: int, cell_type: CellType = CellType.GROUND):
        self.cell_type = cell_type
        self.row = row
        self.col = col
        self.visual = Spot(row, col)
        self.neighbours = {}  # neighbor idx to cell
        self.wood = 0  # if tree -> random from 20 to 100
        self.burned_wood = 0
        self.sector = -1

    def make_fire(self):
        self.cell_type = CellType.FIRE
        self.visual.make_fire(self.wood, self.burned_wood)

    def make_tree(self):
        self.cell_type = CellType.TREE
        self.visual.make_tree(self.wood)

    def make_burned(self):
        self.cell_type == CellType.BURNED
        self.visual.make_burned(self.burned_wood)
