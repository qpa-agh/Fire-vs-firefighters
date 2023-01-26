import pygame
from controller.fire_controller import FireController
from model.model import Model
from model.wind_data import WindDirection
from model.fighter import FighterAction
from solver.decisions_generator import DecisionsGenerator
from view.button_handler import ButtonHandler
from view.view_controller import ViewController, ViewType
from controller.fighters_controller import FightersController
from solver.solver import Solver
import itertools


class SimulationController:
    def __init__(self, model: Model) -> None:
        self.model = model
        self.width = model.get_width()
        self.height = model.get_height()

        self.BUTTON_LIST_WIND = [("NW", WindDirection.NW, (self.width + 25, self.height - 190)),
                                 ("N", WindDirection.N,
                                  (self.width + 94, self.height - 215)),
                                 ("NE", WindDirection.NE,
                                  (self.width + 145, self.height - 190),),
                                 ("E", WindDirection.E,
                                  (self.width + 180, self.height - 125),),
                                 ("SE", WindDirection.SE,
                                  (self.width + 145, self.height - 60)),
                                 ("S", WindDirection.S,
                                  (self.width + 94, self.height - 35)),
                                 ("SW", WindDirection.SW,
                                  (self.width + 25, self.height - 60)),
                                 ("W", WindDirection.W,  (self.width + 5, self.height - 125))]

        self.button_handler_wind = ButtonHandler(self.BUTTON_LIST_WIND)

        self.view_controller = ViewController(self.width, self.height, self.model.gap)
        self.fire_controller = FireController()
        self.fighters_controller = FightersController()

        self.animation_started = False
        self.run = True
        self.iteration = 0
        self.solver = Solver()
        self.decision_generator = DecisionsGenerator()

    def run_simulation(self) -> None:
        A = [[3, 1],
             [0, 2]]
        B = [[2, 1],
             [0, 3]]
        self.solver.solve(A, B)
        pygame.init()
        self.view_controller.draw_buttons(self.button_handler_wind)
        while self.run:
            if self.animation_started:
                # print(self.iteration)
                self.iteration += 1
            self.view_controller.draw_model(self.model, self.iteration)
            self.view_controller.draw_buttons(self.button_handler_wind)
            for event in pygame.event.get():
                self.resolve_event(event)
            self.animation_started = self.fire_controller.spread_fire(
                self.model, self.animation_started)
            self.fighters_controller.run_fighters(
                self.model, self.animation_started)
            self.commander()
            self.view_controller.update()
        pygame.quit()

    def commander(self):

        if self.iteration == 20:
            A, Adec, B, Bdec = self.decision_generator.create_game_price_array(
                self.model)
            print(Adec, Bdec[:50])
            print(len(Bdec))
            self.solver.solve(A[:, :50], B[:, :50])
        if self.iteration == 1:
            for team in self.model.teams:
                team.set_target_action(FighterAction.DIG_DITCH)
        if self.iteration == 300:
            self.model.teams[0].set_target_sector((12, 11))
            self.model.teams[0].set_target_action(FighterAction.DIG_DITCH)
            self.model.teams[1].set_target_sector((12, 12))
            self.model.teams[1].set_target_action(FighterAction.DIG_DITCH)
            self.model.teams[2].set_target_sector((12, 13))
            self.model.teams[2].set_target_action(FighterAction.DIG_DITCH)
            self.model.teams[3].set_target_sector((12, 14))
            self.model.teams[3].set_target_action(FighterAction.DIG_DITCH)
            self.model.teams[4].set_target_sector((12, 15))
            self.model.teams[4].set_target_action(FighterAction.DIG_DITCH)
            self.model.teams[5].set_target_sector((11, 16))
            self.model.teams[5].set_target_action(FighterAction.DIG_DITCH)
            self.model.teams[6].set_target_sector((11, 10))
            self.model.teams[6].set_target_action(FighterAction.DIG_DITCH)

        if self.iteration == 600:
            self.model.teams[0].set_target_sector((11, 11))
            self.model.teams[0].set_target_action(FighterAction.EXTINGUISH)
            self.model.teams[1].set_target_sector((11, 12))
            self.model.teams[1].set_target_action(FighterAction.EXTINGUISH)
            self.model.teams[2].set_target_sector((11, 13))
            self.model.teams[2].set_target_action(FighterAction.EXTINGUISH)
            self.model.teams[3].set_target_sector((11, 14))
            self.model.teams[3].set_target_action(FighterAction.EXTINGUISH)
            self.model.teams[4].set_target_sector((11, 15))
            self.model.teams[4].set_target_action(FighterAction.EXTINGUISH)
            self.model.teams[5].set_target_sector((10, 16))
            self.model.teams[5].set_target_action(FighterAction.EXTINGUISH)
            self.model.teams[6].set_target_sector((10, 10))
            self.model.teams[6].set_target_action(FighterAction.EXTINGUISH)

    def resolve_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self.run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.animation_started = not self.animation_started
            if event.key == pygame.K_c:  # reset
                self.model.reset_model()
                self.animation_started = False
                self.iteration = 0
            if event.key == pygame.K_z:  # change
                self.view_controller.view_type = ViewType.MAP \
                    if self.view_controller.view_type == ViewType.FIRE_FIGHTERS \
                    else ViewType.FIRE_FIGHTERS

            if event.key == pygame.K_i:  # zoom in
                self.view_controller.zoom_in()
            if event.key == pygame.K_o:  # zoom out
                self.view_controller.zoom_out()

            if event.key == pygame.K_w:  # top
                self.view_controller.move_up()
            if event.key == pygame.K_a:  # left
                self.view_controller.move_left()
            if event.key == pygame.K_s:  # bottom
                self.view_controller.move_down()
            if event.key == pygame.K_d:  # right
                self.view_controller.move_right()

        if pygame.mouse.get_pressed()[0]:  # LEFT
            pos = pygame.mouse.get_pos()
            row, col = self.view_controller.get_clicked_pos(pos)

            # if pos is within the model.visual
            if row < self.model.cells_y and col < self.model.cells_x:
                if self.animation_started:
                    return
                self.model.make_spot_fire(row, col)
            else:  # check pushing button
                x, y = pos
                self.model.wind_direction = self.button_handler_wind.click_proper_button(
                    x, y)

                self.view_controller.draw_buttons(self.button_handler_wind)

        elif pygame.mouse.get_pressed()[2]:  # RIGHT
            if self.animation_started:
                return
            pos = pygame.mouse.get_pos()
            row, col = self.view_controller.get_clicked_pos(pos)
            if row < self.model.cells_y and col < self.model.cells_x:
                self.model.reset_spot(row, col)
