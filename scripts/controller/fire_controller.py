import random
from model.model import Model

class WindModifier:
    positive = 4
    close_positive = 2
    negative = 0.25
    close_negative = 0.5


class FireController:
    def __init__(self) -> None:
        self.fire_chance = 0.01
        self.diagonal_fire_modifier = 0.7
        self.wood_burned_per_frame = 0.25
        self.diagonal_keys = set({1, 3, 5, 7})

    def spread_fire(self, model: Model, animation_started: bool) -> bool:
        if not animation_started:
            return False

        new_generation = set()
        for cell in model.cells_on_fire:
            for key, neighbour in cell.neighbours.items():
                if neighbour.is_tree():
                    wind_modifier = self.__get_wind_modifier(
                        model.wind_direction, key)
                    diagonal_modifier = self.diagonal_fire_modifier if key in self.diagonal_keys else 1
                    if random.random() <= self.fire_chance * wind_modifier * diagonal_modifier:
                        neighbour.make_fire()
                        new_generation.add(neighbour)

            cell.burn_wood(self.wood_burned_per_frame)
            if cell.has_wood_to_burn():
                new_generation.add(cell)

        model.cells_on_fire = new_generation
        if not model.cells_on_fire:  # animation ended or not started
            animation_started = False
        return animation_started

    def __get_wind_modifier(self, wind_dir, neigh_dir):
        if wind_dir is None or neigh_dir is None:
            return 1
        left_neigh_dir = (neigh_dir + 7) % 8
        right_neigh_dir = (neigh_dir + 1) % 8
        opposite_wind_dir = (wind_dir + 4) % 8

        if wind_dir == neigh_dir:
            return WindModifier.positive
        elif wind_dir == left_neigh_dir or wind_dir == right_neigh_dir:
            return WindModifier.close_positive
        elif opposite_wind_dir == neigh_dir:
            return WindModifier.negative
        elif opposite_wind_dir == left_neigh_dir or opposite_wind_dir == right_neigh_dir:
            return WindModifier.close_negative
        return 1
