from utils.enums import TreeType
from view.colors import Color
from view.view_params import View
import pygame


class Spot:
    """Representation of the pixel on a grid."""

    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.y = row * View.gap
        self.x = col * View.gap
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
        pygame.draw.rect(View.window, self.color, 
                         ((self.x - View.gap*View.shift_x) *View.zoom_scale,
                         (self.y - View.gap*View.shift_y) * View.zoom_scale, View.gap*View.zoom_scale, 
                         View.gap*View.zoom_scale))

    def make_ground(self):
        self.color = Color.ground

    def make_fire(self, wood, burning_wood, burned_wood):
        stage = int(
            max(burning_wood/(burning_wood + burned_wood + wood), 0) * len(Color.fire))
        if stage >= len(Color.fire):
            stage -= 1
        self.color = Color.fire[stage]

    def make_burned(self, burned_wood: int):
        self.color = Color.burned[int(burned_wood-20)//20]

    def make_tree(self, wood, tree_type: TreeType, moisture: float):
        if tree_type == TreeType.DECIDUOUS:
            self.color = Color.tree[int(wood//20-1)]
        else:
            self.color = Color.tree_col[int(wood//20-1)]

    def make_water(self):
        self.color = Color.water

    def make_grass(self):
        self.color = Color.grass_green