

class FighterTeamCommanderAction:
    def __init__(self) -> None:
        pass

    def run_action(self, model):
        raise NotImplementedError()

class Idle(FighterTeamCommanderAction):
    def __init__(self) -> None:
        super().__init__()

    def run_action(self, model):
        pass

class ChangeTeamOrderAction(FighterTeamCommanderAction):
    def __init__(self) -> None:
        super().__init__()

    def run_action(self, model):
        pass
