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
from view.view_params import View
import sys
sys.setrecursionlimit(100000)


def new_procees_to_solve_nash(conn):
    A, Adec, B, Bdec = conn.recv()
    solver = Solver()
    print("Adec lenght: ", len(Adec), "Bdec lenght: ", len(Bdec))
    actions = solver.solve(A, B, Adec, Bdec)
    print(actions)

    conn.send(actions)
    conn.close()


class SimulationController:
    def __init__(self, model: Model) -> None:
        self.model = model

        self.BUTTON_LIST_WIND = [("NW", WindDirection.NW, (View.width + 35, View.height - 190)),
                                 ("N", WindDirection.N,
                                  (View.width + 104, View.height - 215)),
                                 ("NE", WindDirection.NE,
                                  (View.width + 155, View.height - 190),),
                                 ("E", WindDirection.E,
                                  (View.width + 190, View.height - 125),),
                                 ("SE", WindDirection.SE,
                                  (View.width + 155, View.height - 60)),
                                 ("S", WindDirection.S,
                                  (View.width + 104, View.height - 35)),
                                 ("SW", WindDirection.SW,
                                  (View.width + 35, View.height - 60)),
                                 ("W", WindDirection.W,  (View.width + 10, View.height - 125))]

        self.button_handler_wind = ButtonHandler(self.BUTTON_LIST_WIND)

        self.view_controller = ViewController()
        self.fire_controller = FireController()
        self.fighters_controller = FightersController()

        self.animation_started = False
        self.run = True
        self.iteration = 0

    def get_commanders_actions(self):
        decision_generator = DecisionsGenerator()
        A, Adec, B, Bdec = decision_generator.create_game_price_array(self.model)
        parent_conn, child_conn = Pipe()
        p = Process(target=new_procees_to_solve_nash, args=(child_conn,))
        p.start()
        parent_conn.send([A, Adec, B, Bdec])
        actions = parent_conn.recv()

        while p.is_alive():
            self.resolve_events()
            self.view_controller.update()
            p.join(timeout=0.1)
            print('waiting')
        return actions

    def run_simulation(self) -> None:
        self.view_controller.draw_buttons(self.button_handler_wind)
        while self.run:
            if self.animation_started:
                self.iteration += 1
            self.view_controller.draw_model(self.model, self.iteration)
            self.view_controller.draw_buttons(self.button_handler_wind)

            self.resolve_events()

            self.animation_started = self.fire_controller.spread_fire(
                self.model, self.animation_started)
            self.fighters_controller.run_fighters(
                self.model, self.animation_started)
            if not self.model.cells_on_fire:  # animation ended or not started
                self.animation_started = False
            self.commander()
            self.view_controller.update()
        pygame.quit()

    def commander(self):
        if not self.animation_started:
            return
        if self.iteration % 30 == 16:
            actions = self.get_commanders_actions()
            self.display_actions(actions)
            self.model.apply_actions(actions)

    def resolve_events(self):
        for event in pygame.event.get():
            self.resolve_event(event)

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

    def display_actions(self, actions):
        pass
    #     for action in actions:
    #         print(" --------")
    #         print("Action:")
    #         team, move, pos = action
    #         if team: print("team:", team.target_action, team.target_action)
    #         print("move:", move, "  pos:", pos)
