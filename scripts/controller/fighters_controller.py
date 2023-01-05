from __future__ import annotations
from random import randrange
from model.fighter import FighterAction
from model.model import Model
from utils.enums import Direction


class FightersController:
    def __init__(self) -> None:
        pass

    def run_fighters(self, model: Model, animation_started):
        if not animation_started:
            return
        for team in model.teams:
            team.update_fighters_action_direction()
            team.run_team(model)

