import nashpy as nash
import numpy as np

class Solver:
    def __init__(self) -> None:
        pass

    def solve(self, A, B, Adec, Bdec):
        game = nash.Game(A, B)
        eqs = game.vertex_enumeration()
        eq = next(eqs, None) # throws divide by zero
        if eq is None:
            return []
        return self.__get_actions(eq, Adec, Bdec)

    def __get_actions(self, eq, Adec, Bdec):
        logistics_decision_idx = np.argmax(eq[0])
        team_commander_decision_idx = np.argmax(eq[1])
        return [Adec[logistics_decision_idx], Bdec[team_commander_decision_idx]]

