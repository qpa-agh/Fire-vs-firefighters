from model.fighter import FighterAction
import numpy as np
from utils.enums import LogisticAction


class DecisionsGenerator:
    STANDARD_NUMBER_OF_FIRE_SECTORS_PER_TEAM = 5
    RELUCTANCY_TO_ADDING_TEAM = 20
    INCENTIVE_TO_ADDING_TEAM_FACTOR = 10

    ONLY_FIRE_EXTINGUISH_VALUE = 20
    DIG_VALUE_PER_SECTOR_BEHIND = 1
    DIG_DITCH_DISTANCE_FACTOR = 2

    EXTINGUISH_FIRE_DISTANCE_SQUARED_FACTOR = 3
    EXTINGUISH_VALUE_PER_SECTOR_BEHIND = 1
    EXTINGUISH_CONSTANT = 10

    SECTOR_MOVE_FACTOR = 4

    PRICE_FOR_COMMANDER_FOR_TEAM_CALLBACK = -50

    PARAMETERS_FITTED_FOR_NUMBER_OF_SECTORS = 30

    def __init__(self) -> None:
        pass

    def create_game_price_array(self, model):
        logistic_prices_dict = self.__calculate_logistic_prizes(model)
        team_commander_prices_dict = self.__calculate_team_change_order_prices(model)

        team_commander_prices_dict = self.__cull_worse_decisions(team_commander_prices_dict)
        Adecision, Bdecision = list(logistic_prices_dict.keys()), list(team_commander_prices_dict.keys())

        price_array_shape = (len(logistic_prices_dict), len(team_commander_prices_dict))
        A = np.zeros(price_array_shape)
        B = np.zeros(price_array_shape)
        for y, (row, row_decision_value) in enumerate(logistic_prices_dict.items()):
            for x, (col, col_decision_value) in enumerate(team_commander_prices_dict.items()):
                A[y, x] = row_decision_value
                B[y, x] = col_decision_value
                if row[1] == LogisticAction.FALLBACK_TEAM:
                    B[y, x] += DecisionsGenerator.PRICE_FOR_COMMANDER_FOR_TEAM_CALLBACK
                    if row[0] == col[0]:
                        B[y, x] = DecisionsGenerator.PRICE_FOR_COMMANDER_FOR_TEAM_CALLBACK
                        A[y, x] -= col_decision_value / 2

        return A, Adecision, B, Bdecision

    def __cull_worse_decisions(self, team_commander_prices_dict):
        threshold = np.percentile(list(team_commander_prices_dict.values()), 90)
        return dict((key, value) for key, value in team_commander_prices_dict.items() if value >= threshold)

    def __calculate_logistic_prizes(self, model):
        logistic_order_values = {
            (None, LogisticAction.IDLE, None): 0,
        }

        no_teams = len(model.teams)
        no_sectors_on_fire = len(model.sectors_with_fire)
        incentive_to_fallback_a_team =  - (no_sectors_on_fire - (no_teams - 1) * DecisionsGenerator.STANDARD_NUMBER_OF_FIRE_SECTORS_PER_TEAM) * DecisionsGenerator.INCENTIVE_TO_ADDING_TEAM_FACTOR
        logistic_order_values[(None, LogisticAction.ADD_NEW_TEAM, None)] = - incentive_to_fallback_a_team - DecisionsGenerator.RELUCTANCY_TO_ADDING_TEAM
        for team in model.teams:
            logistic_order_values[(team, LogisticAction.FALLBACK_TEAM, None)] = incentive_to_fallback_a_team

        return logistic_order_values

    def __calculate_team_change_order_prices(self, model):
        teams_order_value = {}
        sector_action_values = self.__calculate_sector_usefullness_dict(model)
        for team in model.teams:
            is_team_useless = team.target_action == FighterAction.IDLE #or team.target_sector not in sector_action_values[team.target_action].keys()
            current_value = -100 if is_team_useless else (0 if team.target_sector not in sector_action_values[team.target_action].keys() else sector_action_values[team.target_action][team.target_sector])
            closest_fire_sector = None if not is_team_useless else self.__find_closest_fire(model, team.target_sector)[0]
            for sector in sector_action_values[FighterAction.EXTINGUISH].keys():
                move_distance = self.__sector_distance(team.target_sector, sector)
                if is_team_useless:
                    distance = self.__sector_distance(closest_fire_sector, sector)
                else:
                    distance = move_distance
                    
                if distance > 3:
                    continue
                teams_order_value[(team, FighterAction.EXTINGUISH, sector)] = sector_action_values[FighterAction.EXTINGUISH][sector] - move_distance * DecisionsGenerator.SECTOR_MOVE_FACTOR - current_value
                teams_order_value[(team, FighterAction.DIG_DITCH, sector)] = sector_action_values[FighterAction.DIG_DITCH][sector] - move_distance * DecisionsGenerator.SECTOR_MOVE_FACTOR - current_value

        return teams_order_value


    def __calculate_sector_usefullness_dict(self, model):
        values = {FighterAction.EXTINGUISH: {}, FighterAction.DIG_DITCH: {}}
        for sector in [*model.flammable_sectors, *model.sectors_with_fire]:
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

    def __find_closest_fire(self, model, sector):
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

    def __calculate_flammable_sectors_behind(self, model, sector, closest_fire_sector):
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

