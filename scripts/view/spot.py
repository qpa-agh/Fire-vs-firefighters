from utils.enums import SectorType, ViewType, TreeType
from view.colors import Color
import pygame


class Spot:
    """Representation of the pixel on a grid."""
    width = None  # spots width = gap between 2 lines
    window = None

    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.x = row * Spot.width
        self.y = col * Spot.width
        self.color = Color.ground
        self.neighbours = []

    def get_pos(self):
        """Returns idx of row and column of the object."""
        return self.row, self.col

    def draw(self):
        """
        Draw the square with proper color and standaralized size in CELL mode, otherways
        draws 10x10 squares.
        """
        pygame.draw.rect( Spot.window, self.color, (self.y, self.x, Spot.width, Spot.width))

    def make_ground(self):
        self.color = Color.ground

    def make_fire(self, wood, burning_wood, burned_wood):
        stage = int(max(burning_wood/(burning_wood + burned_wood + wood), 0) * len(Color.fire))
        if stage >= len(Color.fire):
            stage -= 1
        self.color = Color.fire[stage]

    def make_burned(self, burned_wood: int):
        self.color = Color.burned[int(burned_wood-20)//20]

    def make_tree(self, wood, tree_type: TreeType):
        if tree_type == TreeType.DECIDUOUS:
            self.color = Color.tree[int(wood//20-1)]
        else:
            self.color = Color.tree_col[int(wood//20-1)]
    def make_water(self):
        self.color = Color.water

    @staticmethod
    def set_width(width):
        """Sets global parameters for all dots."""
        Spot.width = width

    @staticmethod
    def set_window(window):
        """Sets global parameters for all dots."""
        Spot.window = window
