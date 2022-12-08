import random
from model.cell import CellType
from model.model import Model


class FireController:
    def __init__(self) -> None:
        self.fire_chance = 0.01
        self.diagonal_fire_modifier = 0.7
        self.wind_positive_modifier = 4
        self.wind_close_positive_modifier = 2
        self.wind_negative_modifier = 0.25
        self.wind_close_negative_modifier = 0.5

    def spread_fire(self, model: Model, animation_started: bool) -> bool:
        if animation_started:
            new_generation = set()
            for cell in model.cells_on_fire:
                for key, neighbour in cell.neighbours.items():
                    if neighbour.cell_type == CellType.TREE:
                        wind_factor = self.__get_wind_factor(
                            model.wind_direction, key)
                        roll = random.random()
                        is_new_fire = roll <= self.fire_chance * \
                            wind_factor * \
                            (self.diagonal_fire_modifier if key in [
                             1, 3, 5, 7] else 1)
                        if is_new_fire:
                            neighbour.make_fire()
                            new_generation.add(neighbour)

                cell.wood -= 0.25
                cell.burned_wood += 0.25
                if cell.wood <= 0:
                    cell.make_burned()
                else:
                    cell.make_fire()
                    new_generation.add(cell)

            model.cells_on_fire = new_generation
            if not model.cells_on_fire:
                animation_started = False
        return animation_started

    def __get_wind_factor(self, wind_dir, neigh_dir):
        if wind_dir is None or neigh_dir is None:
            return 1
        left_neigh_dir = (neigh_dir + 7) % 8
        right_neigh_dir = (neigh_dir + 1) % 8
        opposite_wind_dir = (wind_dir + 4) % 8

        if wind_dir == neigh_dir:
            return self.wind_positive_modifier
        elif wind_dir == left_neigh_dir or wind_dir == right_neigh_dir:
            return self.wind_close_positive_modifier
        elif opposite_wind_dir == neigh_dir:
            return self.wind_negative_modifier
        elif opposite_wind_dir == left_neigh_dir or opposite_wind_dir == right_neigh_dir:
            return self.wind_close_negative_modifier
        return 1
