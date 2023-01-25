from enum import Enum
from math import degrees
from cv2 import sqrt
from model.fighter import FighterAction
from model.model import Model
import numpy as np

class LogisticAction(Enum):
    IDLE = 0
    ADD_NEW_TEAM = 1
    FALLBACK_TEAM = 2


class DecisionsGenerator:
    STANDARD_NUMBER_OF_FIRE_SECTORS_PER_TEAM = 3
    RELUCTANCY_TO_ADDING_TEAM = 20
    INCENTIVE_TO_ADDING_TEAM_FACTOR = 10

    ONLY_FIRE_EXTINGUISH_VALUE = 20
    DIG_VALUE_PER_SECTOR_BEHIND = 1
    DIG_DITCH_DISTANCE_FACTOR = 2

    EXTINGUISH_FIRE_DISTANCE_SQUARED_FACTOR = 3
    EXTINGUISH_VALUE_PER_SECTOR_BEHIND = 1
    EXTINGUISH_CONSTANT = 10

    SECTOR_MOVE_FACTOR = 4

    PARAMETERS_FITTED_FOR_NUMBER_OF_SECTORS = 30

    def __init__(self) -> None:
        pass

    def create_game_price_array(self, model: Model):
        logistic_prices_dict = self.__calculate_logistic_prizes(model)
        team_commander_prices_dict = self.__calculate_team_change_order_prices(model)
        Adecision, Bdecision = list(logistic_prices_dict.keys()), list(team_commander_prices_dict.keys())

        price_array_shape = (len(logistic_prices_dict), len(team_commander_prices_dict))
        A = np.zeros(price_array_shape)
        B = np.zeros(price_array_shape)
        for y, (row, row_decision_value) in enumerate(logistic_prices_dict.items()):
            for x, (col, col_decision_value) in enumerate(team_commander_prices_dict.items()):
                A[y, x] = row_decision_value
                B[y, x] = col_decision_value

        return A, Adecision, B, Bdecision

    def __calculate_logistic_prizes(self, model: Model):
        logistic_order_values = {
            LogisticAction.IDLE: 0,
            LogisticAction.ADD_NEW_TEAM: 0,
            LogisticAction.FALLBACK_TEAM: 0
        }

        no_teams = len(model.teams)
        no_sectors_on_fire = len(model.sectors_with_fire)
        logistic_order_values[LogisticAction.ADD_NEW_TEAM] = (no_sectors_on_fire - no_teams * DecisionsGenerator.STANDARD_NUMBER_OF_FIRE_SECTORS_PER_TEAM) * DecisionsGenerator.INCENTIVE_TO_ADDING_TEAM_FACTOR - DecisionsGenerator.RELUCTANCY_TO_ADDING_TEAM
        logistic_order_values[LogisticAction.FALLBACK_TEAM] = - (no_sectors_on_fire - no_teams * DecisionsGenerator.STANDARD_NUMBER_OF_FIRE_SECTORS_PER_TEAM) * DecisionsGenerator.INCENTIVE_TO_ADDING_TEAM_FACTOR

        return logistic_order_values

    def __calculate_team_change_order_prices(self, model: Model):
        teams_order_value = {}
        sector_action_values = self.__calculate_sector_usefullness_dict(model)
        for team in model.teams:
            current_value = -100 if team.target_action == FighterAction.IDLE else sector_action_values[team.target_action][team.target_sector]
            for sector in sector_action_values[FighterAction.EXTINGUISH].keys():
                distance = self.__sector_distance(team.target_sector, sector)
                teams_order_value[(team, FighterAction.EXTINGUISH, sector)] = sector_action_values[FighterAction.EXTINGUISH][sector] - current_value - distance * DecisionsGenerator.SECTOR_MOVE_FACTOR
                teams_order_value[(team, FighterAction.DIG_DITCH, sector)] = sector_action_values[FighterAction.DIG_DITCH][sector] - current_value - distance * DecisionsGenerator.SECTOR_MOVE_FACTOR

        return teams_order_value


    def __calculate_sector_usefullness_dict(self, model: Model):
        values = {FighterAction.EXTINGUISH: {}, FighterAction.DIG_DITCH: {}}
        for sector in model.flammable_sectors:
            closest_fire_sector, fire_sector_distance = self.__find_closest_fire(model, sector)
            if closest_fire_sector is None:
                values[FighterAction.DIG_DITCH][sector] = 0
                values[FighterAction.EXTINGUISH][sector] = DecisionsGenerator.ONLY_FIRE_EXTINGUISH_VALUE
                continue

            points_for_sectors_behind = self.__calculate_flammable_sectors_behind(model, sector, closest_fire_sector) * DecisionsGenerator.PARAMETERS_FITTED_FOR_NUMBER_OF_SECTORS / (model.sectors_y * model.sectors_x)
            if sector in model.sectors_with_fire:
                values[FighterAction.DIG_DITCH][sector] = 0
                values[FighterAction.EXTINGUISH][sector] = 2 * DecisionsGenerator.EXTINGUISH_CONSTANT + points_for_sectors_behind * DecisionsGenerator.EXTINGUISH_VALUE_PER_SECTOR_BEHIND
                continue

            values[FighterAction.DIG_DITCH][sector] = points_for_sectors_behind *  DecisionsGenerator.DIG_VALUE_PER_SECTOR_BEHIND - fire_sector_distance * DecisionsGenerator.DIG_DITCH_DISTANCE_FACTOR
            values[FighterAction.EXTINGUISH][sector] = DecisionsGenerator.EXTINGUISH_CONSTANT + points_for_sectors_behind * DecisionsGenerator.EXTINGUISH_VALUE_PER_SECTOR_BEHIND - (fire_sector_distance ** 2) * DecisionsGenerator.EXTINGUISH_FIRE_DISTANCE_SQUARED_FACTOR

        return values

    def __find_closest_fire(self, model:Model, sector):
        closest_fire_sector = None
        min_distance = float("inf")
        for fire_sector in model.sectors_with_fire:
            if fire_sector == sector:
                continue
            distance = self.__sector_distance(sector, fire_sector)
            if distance < min_distance:
                min_distance = distance
                closest_fire_sector = fire_sector

        return closest_fire_sector, min_distance

    def __calculate_flammable_sectors_behind(self, model: Model, sector, closest_fire_sector):
        y_sector_distance = sector[0] - closest_fire_sector[0]
        x_sector_distance = sector[1] - closest_fire_sector[1]
        behind_alfa = np.angle(complex(x_sector_distance, y_sector_distance), deg=True) # 0 degrees is x axis

        flammable_sectors_behind = 0
        for flammable_sector in model.flammable_sectors:
            alfa = np.angle(complex(flammable_sector[1] - sector[1], flammable_sector[0] - sector[0]), deg=True)
            angle_diff = (alfa - behind_alfa + 180 + 360) % 360 - 180 # check if flammable sector direction is in a 90 deg arc from target sector
            if angle_diff <= 45 and angle_diff >= -45:
                flammable_sectors_behind += 1

        return flammable_sectors_behind

    def __sector_distance(self, sector1, sector2):
        return np.sqrt((sector1[0] - sector2[0]) ** 2 + (sector1[1] - sector2[1]) ** 2)

