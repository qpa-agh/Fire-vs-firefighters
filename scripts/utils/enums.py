from enum import Enum

class CellType(Enum):
    GROUND = 0,
    TREE = 1,
    FIRE = 2,
    BURNED = 3,
    GRASS = 4

class SectorType(Enum):
    GRASS = 0
    TREES = 1

class ViewType(Enum):
    CELL = 0
    SECTOR = 1
