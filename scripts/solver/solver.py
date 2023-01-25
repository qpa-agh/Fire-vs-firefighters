import nashpy as nash


class Solver:
    def __init__(self) -> None:
        pass

    def solve(self, A, B):
        game = nash.Game(A, B)
        print(game)
        eqs = game.vertex_enumeration()
        for eq in eqs:
            print(eq)

