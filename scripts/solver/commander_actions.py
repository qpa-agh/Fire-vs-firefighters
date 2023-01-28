from model.fighter import FighterAction
from solver.decisions_generator import LogisticAction


class CommanderLogisticAction:
    def __init__(self, action) -> None:
        self.team, self.action_type, self.sector = action

    def run_action(self, model):
        raise NotImplementedError()

    def get_model_team(self, model):
        teams = [team for team in model.teams if team.team_id == self.team.team_id]
        return None if not teams else teams[0]

class Idle(CommanderLogisticAction):
    def __init__(self, action) -> None:
        super().__init__(action)

    def run_action(self, model):
        pass

class LogisticIdle(CommanderLogisticAction):
    def __init__(self, action) -> None:
        super().__init__(action)

    def run_action(self, model):
        pass

class LogisticAddNewTeam(CommanderLogisticAction):
    def __init__(self, action) -> None:
        super().__init__(action)

    def run_action(self, model):
        model.generate_fighters(10, [(0, 0)])

class LogisticFallBackTeam(CommanderLogisticAction):
    def __init__(self, action) -> None:
        super().__init__(action)

    def run_action(self, model):
        team = self.get_model_team(model)
        if team in model.teams:
            model.teams.remove(team)

class CommanderIdle(CommanderLogisticAction):
    def __init__(self, action) -> None:
        super().__init__(action)

    def run_action(self, model):
        pass

class CommanderChangeTeamOrderAction(CommanderLogisticAction):
    def __init__(self, action) -> None:
        super().__init__(action)

    def run_action(self, model):
        team = self.get_model_team(model)
        if team is not None:
            team.set_target_sector(self.sector)
            team.set_target_action(self.action_type)

class CommanderLogisticActionFactory:
    def __init__(self) -> None:
        pass

    def create_action(self, action) -> CommanderLogisticAction:
        action_type = action[1]
        if isinstance(action_type, LogisticAction):
            if action_type == LogisticAction.IDLE:
                return LogisticIdle(action)
            if action_type == LogisticAction.ADD_NEW_TEAM:
                return LogisticAddNewTeam(action)
            if action_type == LogisticAction.FALLBACK_TEAM:
                return LogisticFallBackTeam(action)
        else:
            if action_type == FighterAction.IDLE:
                return LogisticIdle(action)
            if action_type == FighterAction.DIG_DITCH or action_type == FighterAction.EXTINGUISH:
                return CommanderChangeTeamOrderAction(action)

        return Idle(action)