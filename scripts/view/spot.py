from utils.enums import SectorType, ViewType
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

    def draw(self, viewType: ViewType, sector: SectorType):
        """
        Draw the square with proper color and standaralized size in CELL mode, otherways
        draws 10x10 squares.
        """
        if viewType == ViewType.CELL:
            pygame.draw.rect(
                Spot.window, self.color, (self.y, self.x, Spot.width, Spot.width))
        else:
            col = None
            if sector == SectorType.GRASS:
                col = Color.grass_green
            elif sector == SectorType.WATER:
                col = Color.water
            else:
                col = Color.tree[0]
            pygame.draw.rect(
                Spot.window, col, (self.y, self.x, Spot.width, Spot.width))

    def make_fire(self, wood, burned_wood):
        stage = int(burned_wood/(burned_wood + wood) * len(Color.fire))
        if stage >= len(Color.fire):
            stage -= 1
        self.color = Color.fire[stage]

    def make_burned(self, burned_wood: int):
        self.color = Color.burned[int(burned_wood-20)//20]

    def make_tree(self, wood: int):
        self.color = Color.tree[wood//20-1]
    
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
