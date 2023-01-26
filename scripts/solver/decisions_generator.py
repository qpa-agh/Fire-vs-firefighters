from model.fighter import FighterAction
import numpy as np
from utils.enums import LogisticAction


class DecisionsGenerator:
    STANDARD_NUMBER_OF_FIRE_SECTORS_PER_TEAM = 5
    RELUCTANCY_TO_ADDING_TEAM = 20
    INCENTIVE_TO_ADDING_TEAM_FACTOR = 10

    ONLY_FIRE_EXTINGUISH_VALUE = 20
    DIG_VALUE_PER_SECTOR_BEHIND = 1
    DIG_DITCH_DISTANCE_FACTOR = 7
    DIG_VALUE_FOR_BEING_ON_FIRE = - 100

    EXTINGUISH_FIRE_DISTANCE_SQUARED_FACTOR = 2
    EXTINGUISH_VALUE_PER_SECTOR_BEHIND = 1
    EXTINGUISH_VALUE_PER_NEIGHBOURING_SECTOR = 5
    EXTINGUISH_VALUE_FOR_BEING_ON_FIRE = - 100
    EXTINGUISH_CONSTANT = 10

    SECTOR_MOVE_FACTOR = 4

    PRICE_FOR_COMMANDER_FOR_TEAM_CALLBACK = -50

    PARAMETERS_FITTED_FOR_NUMBER_OF_SECTORS = 30

    def __init__(self) -> None:
        pass

    def create_game_price_array(self, model):
        '''Main function that generates game arrays
            A - logisitc player array
            B - fire fighters commander player array
        '''
        logistic_prices_dict = self.__calculate_logistic_prizes(model)
        team_commander_prices_dict = self.__calculate_team_change_order_prices(
            model)

        team_commander_prices_dict = self.__cull_worse_decisions(
            team_commander_prices_dict)
        Adecision, Bdecision = list(logistic_prices_dict.keys()), list(
            team_commander_prices_dict.keys())

        price_array_shape = (len(logistic_prices_dict),
                             len(team_commander_prices_dict))
        A = np.zeros(price_array_shape)
        B = np.zeros(price_array_shape)
        for y, (row, row_decision_value) in enumerate(logistic_prices_dict.items()):
            for x, (col, col_decision_value) in enumerate(team_commander_prices_dict.items()):
                A[y, x] = row_decision_value
                B[y, x] = col_decision_value

                team_logistic, team_commander = row[0], col[0]
                decision_logistic = row[1]
                if decision_logistic == LogisticAction.FALLBACK_TEAM:
                    B[y, x] += DecisionsGenerator.PRICE_FOR_COMMANDER_FOR_TEAM_CALLBACK
                    if team_logistic == team_commander:
                        B[y, x] = DecisionsGenerator.PRICE_FOR_COMMANDER_FOR_TEAM_CALLBACK
                        A[y, x] -= col_decision_value / 2

        return A, Adecision, B, Bdecision

    def __cull_worse_decisions(self, team_commander_prices_dict):
        '''Delete 90% of weakest'''
        threshold = np.percentile(
            list(team_commander_prices_dict.values()), 90)
        return dict((key, value) for key, value in team_commander_prices_dict.items() if value >= threshold)
    
    def compute_necessary_teams(self, sectors_on_fire) -> int:
        if sectors_on_fire <= 2:
            return 1
        elif sectors_on_fire <= 9:
            return int(sectors_on_fire//4)
        elif sectors_on_fire <= 20:
            return int(sectors_on_fire//5)
        elif sectors_on_fire <= 40:
            return int(sectors_on_fire//6)
        elif sectors_on_fire <= 56:
            return int(sectors_on_fire//7)
        else:
            return int(sectors_on_fire//8)

    def __calculate_logistic_prizes(self, model):
        logistic_order_values = {
            (None, LogisticAction.IDLE, None): 0,
        }

        nr_of_teams = len(model.teams)
        nr_of_sectors_on_fire = len(model.sectors_with_fire)

        # motivation to withdraw a team
        teams_shortage = nr_of_sectors_on_fire - nr_of_teams
        print("sectors on fire: ", nr_of_sectors_on_fire,
              " teams: ", nr_of_teams)
        if teams_shortage <= -1: # fallback
            logistic_order_values[(
                None, LogisticAction.ADD_NEW_TEAM, None)] = -500
            incentive_to_fallback_a_team = 100
        
        # idle
        # elif nr_of_teams >= nr_of_sectors_on_fire//4 or teams_shortage <= int(nr_of_sectors_on_fire*0.6) or (teams_shortage <= 5 and nr_of_teams >= 2):
        elif nr_of_teams >= self.compute_necessary_teams(nr_of_sectors_on_fire):
            logistic_order_values[(
                None, LogisticAction.ADD_NEW_TEAM, None)] = -500
            incentive_to_fallback_a_team = -100

        else:  # necessary to add new team
            logistic_order_values[(
                None, LogisticAction.ADD_NEW_TEAM, None)] = 100
            incentive_to_fallback_a_team = -500

        print("Add new team: ", logistic_order_values[(
            None, LogisticAction.ADD_NEW_TEAM, None)])

        for team in model.teams:
            logistic_order_values[(
                team, LogisticAction.FALLBACK_TEAM, None)] = incentive_to_fallback_a_team

        return logistic_order_values

    def __calculate_team_change_order_prices(self, model):
        teams_order_value = {}
        sector_action_values = self.__calculate_sector_usefullness_dict(model)
        for team in model.teams:
            is_team_useless = team.target_action == FighterAction.IDLE #or team.target_sector not in sector_action_values[team.target_action].keys()
            current_value = -100 if is_team_useless else (0 if team.target_sector not in sector_action_values[team.target_action].keys() else sector_action_values[team.target_action][team.target_sector])
            closest_fire_sector, closest_fire_distance = (None, 1000) if not is_team_useless else self.__find_closest_fire(model, team.target_sector)
            
            teams_sectors = [team1.target_sector for team1 in model.teams if team1 != team]
            for sector in sector_action_values[FighterAction.EXTINGUISH].keys():
                closest_fire_sector_to_target_sector, closest_fire_distance_to_target_sector = self.__find_closest_fire(model, sector)

                move_distance = self.__sector_distance(team.target_sector, sector)
                if is_team_useless:
                    distance = self.__sector_distance(
                        closest_fire_sector, sector)
                else:
                    distance = move_distance
                    
                if closest_fire_distance_to_target_sector > 4 or sector in teams_sectors:
                    continue
                teams_order_value[(team, FighterAction.EXTINGUISH, sector)] = sector_action_values[FighterAction.EXTINGUISH][sector] - move_distance * DecisionsGenerator.SECTOR_MOVE_FACTOR - current_value
                teams_order_value[(team, FighterAction.DIG_DITCH, sector)] = sector_action_values[FighterAction.DIG_DITCH][sector] - move_distance * DecisionsGenerator.SECTOR_MOVE_FACTOR - current_value

        return teams_order_value

    def __calculate_sector_usefullness_dict(self, model):
        values = {FighterAction.EXTINGUISH: {}, FighterAction.DIG_DITCH: {}}
        for sector in tuple([*model.flammable_sectors, *model.sectors_with_fire, *[team.target_sector for team in model.teams]]):
            closest_fire_sector, fire_sector_distance = self.__find_closest_fire(model, sector)
            if closest_fire_sector is None:
                values[FighterAction.DIG_DITCH][sector] = 0
                values[FighterAction.EXTINGUISH][sector] = 0
                continue

            points_for_sectors_behind = self.__calculate_flammable_sectors_behind(model, sector, closest_fire_sector) * DecisionsGenerator.PARAMETERS_FITTED_FOR_NUMBER_OF_SECTORS / (model.sectors_y * model.sectors_x)
            neighbouring_sectors_with_fire = self.__calculate_close_fire_sectors(model, sector)
            if sector in model.sectors_with_fire:
                values[FighterAction.DIG_DITCH][sector] = DecisionsGenerator.DIG_VALUE_FOR_BEING_ON_FIRE
                values[FighterAction.EXTINGUISH][sector] = DecisionsGenerator.EXTINGUISH_CONSTANT + points_for_sectors_behind * DecisionsGenerator.EXTINGUISH_VALUE_PER_SECTOR_BEHIND +  DecisionsGenerator.EXTINGUISH_VALUE_FOR_BEING_ON_FIRE + neighbouring_sectors_with_fire * DecisionsGenerator.EXTINGUISH_VALUE_PER_NEIGHBOURING_SECTOR
                continue

            values[FighterAction.DIG_DITCH][sector] = points_for_sectors_behind *  DecisionsGenerator.DIG_VALUE_PER_SECTOR_BEHIND - fire_sector_distance * DecisionsGenerator.DIG_DITCH_DISTANCE_FACTOR
            values[FighterAction.EXTINGUISH][sector] = DecisionsGenerator.EXTINGUISH_CONSTANT + points_for_sectors_behind * DecisionsGenerator.EXTINGUISH_VALUE_PER_SECTOR_BEHIND - (fire_sector_distance ** 2) * DecisionsGenerator.EXTINGUISH_FIRE_DISTANCE_SQUARED_FACTOR  + neighbouring_sectors_with_fire * DecisionsGenerator.EXTINGUISH_VALUE_PER_NEIGHBOURING_SECTOR

        return values

    def __calculate_close_fire_sectors(self, model, sector):
        count = 0
        for fire_sector in model.sectors_with_fire:
            if abs(fire_sector[0] - sector[0]) <= 1 and abs(fire_sector[1] - sector[1]) <= 1:
                count += 1
        return count

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
        # 0 degrees is x axis
        behind_alfa = np.angle(
            complex(x_sector_distance, y_sector_distance), deg=True)

        flammable_sectors_behind = 0
        for flammable_sector in model.flammable_sectors:
            alfa = np.angle(complex(
                flammable_sector[1] - sector[1], flammable_sector[0] - sector[0]), deg=True)
            # check if flammable sector direction is in a 90 deg arc from target sector
            angle_diff = (alfa - behind_alfa + 180 + 360) % 360 - 180
            if angle_diff <= 45 and angle_diff >= -45:
                flammable_sectors_behind += 1

        return flammable_sectors_behind

    def __sector_distance(self, sector1, sector2):
        return np.sqrt((sector1[0] - sector2[0]) ** 2 + (sector1[1] - sector2[1]) ** 2)
