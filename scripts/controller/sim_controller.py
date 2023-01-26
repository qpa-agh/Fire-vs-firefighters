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
from multiprocessing import Process, Pipe
import sys
sys.setrecursionlimit(100000)


def new_procees_to_solve_nash(conn):
    A, Adec, B, Bdec = conn.recv()
    solver = Solver()
    print(len(Adec))
    print(len(Bdec))
    actions = solver.solve(A, B, Adec, Bdec)
    print(actions)

    conn.send(actions)
    conn.close()


class SimulationController:
    def __init__(self, model: Model) -> None:
        self.model = model
        self.BUTTON_LIST = [("NW", WindDirection.NW,
                             (self.model.width + 25, self.model.width - 190)),
                            ("N", WindDirection.N,
                             (self.model.width + 94, self.model.width - 215)),
                            ("NE", WindDirection.NE,
                             (self.model.width + 145, self.model.width - 190),),
                            ("E", WindDirection.E, (self.model.width +
                             180, self.model.width - 125),),
                            ("SE", WindDirection.SE,
                             (self.model.width + 145, self.model.width - 60)),
                            ("S", WindDirection.S,
                             (self.model.width + 94, self.model.width - 35)),
                            ("SW", WindDirection.SW,
                             (self.model.width + 25, self.model.width - 60)),
                            ("W", WindDirection.W,  (self.model.width + 5, self.model.width - 125))]

        self.button_handler = ButtonHandler(
            self.BUTTON_LIST, model.width + 10)
        self.view_controller = ViewController(self.model.width)
        self.fire_controller = FireController()
        self.fighters_controller = FightersController()

        self.animation_started = False
        self.run = True
        self.iteration = 0

    def get_commanders_actions(self):
        decision_generator = DecisionsGenerator()
        A, Adec, B, Bdec = decision_generator.create_game_price_array(self.model)
        # A = [[3, 1], 
        #      [0, 2]]
        # B = [[2, 1], 
        #      [0, 3]]
        # Adec = ['0', '1'] 
        # Bdec = ['0', '1'] 
        parent_conn, child_conn = Pipe()
        p = Process(target=new_procees_to_solve_nash, args=(child_conn,))
        p.start()
        parent_conn.send([A, Adec, B, Bdec])
        actions = parent_conn.recv()

        while p.is_alive():
            for event in pygame.event.get():
                self.resolve_event(event)
            p.join(timeout=0.1)
            print('waiting')
        return actions

    def run_simulation(self) -> None:
        pygame.init()
        self.view_controller.draw_buttons(self.button_handler)
        while self.run:
            if self.animation_started:
                # print(self.iteration)
                self.iteration += 1
            self.view_controller.draw_model(self.model, self.iteration)
            for event in pygame.event.get():
                self.resolve_event(event)
            self.animation_started = self.fire_controller.spread_fire(
                self.model, self.animation_started)
            self.fighters_controller.run_fighters(self.model, self.animation_started)
            self.commander()
            self.view_controller.update()
        pygame.quit()

    def commander(self):
        if self.iteration % 30 == 16:
            actions = self.get_commanders_actions()
            print(actions)
            self.model.apply_actions(actions)
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
                self.model.wind_direction = self.button_handler.click_proper_button(
                    x, y)
                self.view_controller.draw_buttons(self.button_handler)

        elif pygame.mouse.get_pressed()[2]:  # RIGHT
            if self.animation_started:
                return
            pos = pygame.mouse.get_pos()
            row, col = self.view_controller.get_clicked_pos(pos)
            if row < self.model.cells_y and col < self.model.cells_x:
                self.model.reset_spot(row, col)
