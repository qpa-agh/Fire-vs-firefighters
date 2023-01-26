from enum import Enum
import pygame
from model.model import Model
from utils.enums import ViewType
from view.button import Button
from view.spot import Spot
from view.button_handler import ButtonHandler
from view.colors import Color


class ViewController:
    def __init__(self, width, height, gap) -> None:
        self.width = width
        self.height = height
        self.gap = gap
        self.win = pygame.display.set_mode((self.width + 200, self.height))
        Spot.set_window(self.win)
        Button.set_window(self.win)
        pygame.display.set_caption("Fire figters vs fire")
        self.win.fill(Color.white)
        self.view_type = ViewType.MAP
        self.zoom_scale = 1
        self.max_zoom_scale = 8
        self.min_zoom_scale = 1
        self.start_cell_x = 0
        self.start_cell_y = 0

    def draw_model(self, model: Model, iteration):
        """Draws square grid with colored spots."""
        # print("y,x: ",len(model.grid), len(model.grid[0]))
        for y in range(self.start_cell_y, len(model.grid)):
            for x in range(self.start_cell_x, len(model.grid[0])):
                model.grid[y][x].visual.draw(
                    self.zoom_scale, self.start_cell_y, self.start_cell_x)
        self.draw_panel()
        if self.view_type == ViewType.FIRE_FIGHTERS:
            self.draw_fog()
            for team in model.teams:
                self.draw_fighters(team.fighters)

        self.draw_compass()
        self.draw_time(iteration)

    def draw_fighters(self, fighters):
        for fighter in fighters:
            fighter.draw(Spot.window, Spot.width, Spot.width)

    def draw_fog(self):
        """Add a layer of gray fog to enable fire figthers more cleaner visualization."""
        shape_surf = pygame.Surface(pygame.Rect(
            (0, 0, self.width, self.width)).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, Color.fog, shape_surf.get_rect())
        Spot.window.blit(shape_surf, (0, 0, self.width, self.width))

    def draw_buttons(self, button_handler: ButtonHandler):
        """Draws all buttons from list."""
        for button in button_handler.buttons:
            button.draw()
        self.draw_compass()

    def draw_compass(self):
        """Draws compass image."""
        imp = pygame.image.load(
            "scripts\img\compass_small.png").convert_alpha()
        self.win.blit(imp, (self.width + 25, self.height - 190))

    def draw_time(self, iteration):
        pygame.draw.rect(Button.window, Color.white, [
            self.width + 25, self.height - 300, 180, 20])
        smallfont = pygame.font.SysFont('Verdana', 16)
        text = smallfont.render("Time: " + "{:.2f}".format(iteration / 15) + " min", True, Color.black)  # 360 it -> 12 min
        Button.window.blit(text, (self.width + 25, self.height - 300))

    def update(self):
        pygame.display.update()

    def get_clicked_pos(self, pos) -> tuple():
        """Returns row and columns idx of clicked place."""
        x, y = pos
        row = y // Spot.width
        col = x // Spot.width
        return row, col
    
    def zoom_in(self):
        if self.zoom_scale < self.max_zoom_scale:
            self.zoom_scale = int(2*self.zoom_scale)
        else:
            print("max zoom was reached")
        print("zoom: ", self.zoom_scale)
    
    def zoom_out(self):
        if self.zoom_scale >  1:
            self.zoom_scale = int(self.zoom_scale//2)
        else:
            print("min zoom was reached")
        print("zoom: ", self.zoom_scale)
    
    def draw_panel(self):
        shape_surf = pygame.Surface(pygame.Rect(
            (0, 0, 200, self.height)).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, Color.white, shape_surf.get_rect())
        self.win.blit(shape_surf, (self.width, 0, self.width, self.height))
    
    def move_up(self):
        if self.start_cell_y == self.width - 1:
            return
        self.start_cell_y -= 1
        print("up", self.start_cell_y, self.start_cell_x)
    
    def move_down(self):
        if self.start_cell_y == 0:
            return
        self.start_cell_y += 1
        print("down", self.start_cell_y, self.start_cell_x)
    
    def move_left(self):
        if self.start_cell_x == self.width - 1:
            return
        self.start_cell_x += 1
        print("left", self.start_cell_y, self.start_cell_x)
    
    def move_right(self):
        if self.start_cell_x == 0:
            return
        self.start_cell_x -= 1
        print("right", self.start_cell_y, self.start_cell_x)
