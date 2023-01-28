from __future__ import annotations
from enum import Enum
from random import randrange

import pygame
from utils.enums import Direction, CellType

from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from model.model import Model
    from model.cell import Cell
from view.view_params import View

def moveAction(fighter: Fighter, model: Model) -> None:
    fighter.move_to_target()

def digDitchAction(fighter: Fighter, model: Model) -> None:
    cell = fighter.get_target_cell(model, (1, 1))
    if cell is None or cell.cell_type != CellType.TREE:
        return
    cell.dig_ditch(Fighter.DITCH_MAKING_SPEED)

def extinguishAction(fighter: Fighter, model: Model) -> None:
    cell = fighter.get_target_cell(model, (1, 1))
    if cell is None:
        return
    cell.extinguish(Fighter.EXTINGUISHING_SPEED, Fighter.EXTINGUISHING_MOISTURE_INCREASE)

def idle(fighter: Fighter, model: Model) -> None:
    return

class FighterAction(Enum):
    IDLE: Callable[[Fighter, Model], None] = idle
    MOVE: Callable[[Fighter, Model], None] = moveAction
    DIG_DITCH: Callable[[Fighter, Model], None] = digDitchAction
    EXTINGUISH: Callable[[Fighter, Model], None] = extinguishAction

    @staticmethod
    def random_action() -> FighterAction:
        map = [
            FighterAction.IDLE,
            FighterAction.MOVE,
            FighterAction.DIG_DITCH,
            FighterAction.EXTINGUISH,
        ]
        return map[randrange(0, 4)]

class Fighter:
    DITCH_MAKING_SPEED = 15
    EXTINGUISHING_SPEED = 30
    EXTINGUISHING_MOISTURE_INCREASE = 0.1

    def __init__(self, y: int, x: int, bounds: tuple[int], action: FighterAction = FighterAction.IDLE, direction: Direction = Direction.NW, move_every_n_action = 3) -> None:
        self.y = y
        self.x = x
        self.action = action
        self.direction = direction
        self.bounds = bounds
        self.move_every_n_action = move_every_n_action
        self.n_action = 0
        self.moving_to_different_sector = False
        self.ignore_bounds = False

    def set_sector(self, sector):
        self.bounds =  sector[0] * 10, (sector[0] + 1) * 10, sector[1] * 10, (sector[1] + 1) * 10

    def set_action(self, new_action, ignore_bounds=False):
        self.action = new_action
        self.ignore_bounds = ignore_bounds

    def set_direction(self, new_direction):
        self.direction = new_direction

    def run_action(self, model):
        if self.action not in [FighterAction.IDLE, FighterAction.MOVE]:
            if self.n_action % self.move_every_n_action == 0:
                FighterAction.MOVE(self, model)
            else:
                self.action(self, model)
            self.n_action += 1
        else:
            self.action(self, model)
            self.n_action = 0

    def get_target_cell(self, model: Model, padding: tuple[int] = (0, 0)) -> Cell:
        target_y, target_x = self.y + self.direction[0], self.x + self.direction[1]
        if not self.target_in_bounds(target_y, target_x, padding):
            return model.grid[self.y][self.x]
        return model.grid[target_y][target_x]

    def move_to_target(self) -> None:
        target_y, target_x = self.y + self.direction[0], self.x + self.direction[1]
        if not self.ignore_bounds and not self.target_in_bounds(target_y, target_x):
            return
        self.y = target_y
        self.x = target_x
    
    def target_in_bounds(self, target_y, target_x, padding: tuple[int] = (0, 0)):
        if target_y < self.bounds[0] - padding[0] or \
                target_y >= self.bounds[1] + padding[0] or \
                target_x < self.bounds[2] - padding[1] or \
                target_x >= self.bounds[3] + padding[1]:
            return False
        return True
    
    def draw(self):
        pygame.draw.rect(View.window, (255, 255, 0), ((self.x - View.shift_x)* View.gap*View.zoom_scale,
                         (self.y - View.shift_y) * View.gap*View.zoom_scale, View.gap*View.zoom_scale, View.gap*View.zoom_scale))

    def in_sector(self, sector):
        bounds = sector[0] * 10, (sector[0] + 1) * 10, sector[1] * 10, (sector[1] + 1) * 10
        return not (self.y < bounds[0] or self.y >= bounds[1] or self.x < bounds[2] or self.x >= bounds[3])

