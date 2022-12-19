from enum import Enum

class CellType(Enum):
    GROUND = 0,
    TREE = 1,
    FIRE = 2,
    BURNED = 3,
    GRASS = 4,
    WATER = 5

class SectorType(Enum):
    GRASS = 0
    TREES = 1
    WATER = 2

class ViewType(Enum):
    MAP = 0,
    FIRE_FIGHTERS = 1
