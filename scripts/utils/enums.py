from __future__ import annotations
from enum import Enum
from random import randrange

class CellType(Enum):
    GROUND = 0,
    TREE = 1,
    FIRE = 2,
    BURNED = 3,
    GRASS = 4,
    WATER = 5,


class SectorType(Enum):
    GRASS = 0
    TREES = 1
    WATER = 2


class ViewType(Enum):
    MAP = 0,
    FIRE_FIGHTERS = 1


class TreeType(Enum):
    DECIDUOUS = 0,  # WITH LEAVES
    CONIFEROUS = 1

class LogisticAction(Enum):
    IDLE = 0
    ADD_NEW_TEAM = 1
    FALLBACK_TEAM = 2


class Direction:
    NW = (-1, -1)
    N  = (-1,  0)
    NE = (-1,  1)
    E  = ( 0,  1)
    SE = ( 1,  1)
    S  = ( 1,  0)
    SW = ( 1, -1)
    W  = ( 0, -1)

    @staticmethod
    def random_direction() -> Direction:
        map = {
            0: Direction.NW,
            1: Direction.N,
            2: Direction.NE,
            3: Direction.E,
            4: Direction.SE,
            5: Direction.S,
            6: Direction.SW,
            7: Direction.W,
        }
        return map[randrange(0, 8)]
