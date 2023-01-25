

class FighterMainCommanderAction:
    def __init__(self) -> None:
        pass

    def run_action(self, model):
        raise NotImplementedError()

class Idle(FighterMainCommanderAction):
    def __init__(self) -> None:
        super().__init__()

    def run_action(self, model):
        pass

class AddNewTeam(FighterMainCommanderAction):
    def __init__(self) -> None:
        super().__init__()

    def run_action(self, model):
        pass

class FallBackTeam(FighterMainCommanderAction):
    def __init__(self) -> None:
        super().__init__()

    def run_action(self, model):
        pass
