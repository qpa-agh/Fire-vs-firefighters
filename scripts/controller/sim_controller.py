import pygame
from controller.fire_controller import FireController
from model.model import Model
from model.wind_data import WindDirection
from view.button_handler import ButtonHandler
from view.view_controller import ViewController

BUTTON_LIST = [("NW", WindDirection.NW),
               ("N", WindDirection.N),
               ("NE", WindDirection.NE),
               ("E", WindDirection.E),
               ("SE", WindDirection.SE),
               ("S", WindDirection.S),
               ("SW", WindDirection.SW),
               ("W", WindDirection.W)]


class SimulationController:
    def __init__(self, model: Model) -> None:
        self.model = model
        self.button_handler = ButtonHandler(
            BUTTON_LIST, model.width + 10)
        self.view_controller = ViewController(self.model.width)
        self.fire_controller = FireController()
        self.animation_started = False
        self.run = True

    def run_simulation(self) -> None:
        pygame.init()
        self.view_controller.draw_buttons(self.button_handler)
        while self.run:
            self.view_controller.draw_model(self.model)
            for event in pygame.event.get():
                self.resolve_event(event)
            self.animation_started = self.fire_controller.spread_fire(
                self.model, self.animation_started)
            self.view_controller.update()
        pygame.quit()

    def resolve_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self.run = False
        if not self.animation_started:
            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = self.view_controller.get_clicked_pos(pos)

                # if pos is within the model.visual
                if row < self.model.cells_y and col < self.model.cells_x:
                    self.model.make_spot_fire(row, col)
                else:  # check pushing button
                    x, y = pos
                    self.model.wind_direction = self.button_handler.click_proper_button(
                        x, y)
                    print("wind direction changed:", self.model.wind_direction)
                    self.view_controller.draw_buttons(self.button_handler)

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = self.view_controller.get_clicked_pos(pos)
                if row < self.model.cells_y and col < self.model.cells_x:
                    self.model.reset_spot(row, col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.animation_started = True
                if event.key == pygame.K_c:  # reset
                    self.model.reset_model()
