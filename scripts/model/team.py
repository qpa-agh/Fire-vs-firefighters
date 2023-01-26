

from model.fighter import FighterAction
from utils.enums import Direction


class Team:
    no_teams = 0
    def __init__(self, fighters, target_sector) -> None:
        self.team_id = Team.no_teams
        Team.no_teams += 1

        self.fighters = fighters
        self.target_sector = target_sector
        self.target_action = FighterAction.IDLE
        self.move_team = (0, 0)

    def set_target_sector(self, target_sector):
        self.move_team = (self.move_team[0] + (target_sector[0] - self.target_sector[0]) * 10, self.move_team[1] + (target_sector[1] - self.target_sector[1]) * 10)
        self.target_sector = target_sector

    def set_target_action(self, target_action):
        self.target_action = target_action

    def update_fighters_action_direction(self):
        team_direction = self.__direction_from_move()
        self.move_team = (self.move_team[0] - team_direction[0], self.move_team[1] - team_direction[1])
        for fighter in self.fighters:
            if team_direction != (0, 0):
                if self.move_team == (0, 0):
                    fighter.set_sector(self.target_sector)
                fighter.set_action(FighterAction.MOVE, ignore_bounds=True)
                fighter.set_direction(team_direction)
            else:
                fighter.set_action(self.target_action)
                fighter.set_direction(Direction.random_direction())

    def run_team(self, model):
        print(f'Id: {self.team_id}, action: {self.target_action}, target_sector: {self.target_sector}, move: {self.move_team}')
        for fighter in self.fighters:
            fighter.run_action(model)

    def __direction_from_move(self):
        dir_y = 0 if self.move_team[0] == 0 else self.move_team[0] // abs(self.move_team[0])
        dir_x = 0 if self.move_team[1] == 0 else self.move_team[1] // abs(self.move_team[1])
        return (dir_y, dir_x)
