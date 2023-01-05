import random
from model.model import Model


class WindModifier:
    positive = 1
    close_positive = 0.7
    negative = 0.05
    close_negative = 0.15
    no_wind = 0.5


class FireController:
    def __init__(self) -> None:
        self.diagonal_fire_modifier = 0.7
        self.diagonal_keys = set({1, 3, 5, 7})

    def spread_fire(self, model: Model, animation_started: bool) -> bool:
        if not animation_started:
            return False

        new_generation = set()
        for cell in model.cells_on_fire:
            if not cell.is_on_fire():
                continue
            for key, neighbour in cell.neighbours.items():
                if neighbour.is_tree():
                    wind_modifier = self.__get_wind_modifier(
                        model.wind_direction, key)
                    diagonal_modifier = self.diagonal_fire_modifier if key in self.diagonal_keys else 1
                    wood_factor = cell.burning_wood/100  # how much wood is burning
                    if random.random() <= wind_modifier * diagonal_modifier * wood_factor:
                        if neighbour.moisture <= 0.3:
                            neighbour.make_fire(model.burning_spread_per_frame)
                            new_generation.add(neighbour)
                        else:
                            neighbour.evaporate(model.water_evaporation_per_frame)

            cell.burn_wood(model.wood_burned_per_frame,
                           model.burning_spread_per_frame)
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
        return WindModifier.no_wind
