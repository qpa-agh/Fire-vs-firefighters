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
        Spot.set_width(self.gap)
        self.win = pygame.display.set_mode((self.width + 200, self.height))
        Spot.set_window(self.win)
        Button.set_window(self.win)
        pygame.display.set_caption("Fire figters vs fire")
        self.win.fill(Color.white)
        self.view_type = ViewType.MAP
        self.zoom_scale = 1
        self.max_zoom_scale = 8
        self.min_zoom_scale = 1
        self.shift_x = 0
        self.shift_y = 0
        self.shift_step = 10 # how many cells to shiht when moving

    def draw_model(self, model: Model, iteration):
        """Draws square grid with colored spots."""
        for y in range(self.shift_y, len(model.grid)):
            for x in range(self.shift_x, len(model.grid[0])):
                model.grid[y][x].visual.draw(
                    self.zoom_scale, self.shift_y, self.shift_x)
        self.draw_panel()
        if self.view_type == ViewType.FIRE_FIGHTERS:
            self.draw_fog()
            for team in model.teams:
                self.draw_fighters(team.fighters)
                smallfont = pygame.font.SysFont('Verdana', 24)
                text = smallfont.render(str(team.team_id), True, Color.white)
                Spot.window.blit(text, ((team.target_sector[1] * 10 + 2) * self.gap, (team.target_sector[0] * 10 + 2) * self.gap))

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
        row = y // Spot.width // self.zoom_scale + self.shift_y
        col = x // Spot.width // self.zoom_scale + self.shift_x
        return row, col
    
    def zoom_in(self):
        """Zoom in the view with factor = 2. Max and zoom scales are defined in constructor."""
        if self.zoom_scale < self.max_zoom_scale:
            self.zoom_scale = int(2*self.zoom_scale)
    
    def zoom_out(self):
        """Zoom out the view with factor = 2. Max and zoom scales are defined in constructor."""
        if self.zoom_scale >  1:
            self.zoom_scale = int(self.zoom_scale//2)
        
        relative_height = self.height // self.gap // self.zoom_scale
        if self.shift_y + relative_height >= self.height//self.gap - self.zoom_scale*2:
            self.shift_y = self.height//self.gap - self.zoom_scale*2 - relative_height
        
        relative_width = self.width // self.gap // self.zoom_scale
        if self.shift_x + relative_width >= (self.width)//self.gap - self.zoom_scale*2:
            self.shift_x = (self.width)//self.gap - \
                self.zoom_scale*2 - relative_width
        
        if self.zoom_scale == 1:
            self.shift_x = 0
            self.shift_y = 0
    
    def draw_panel(self):
        shape_surf = pygame.Surface(pygame.Rect(
            (0, 0, 200, self.height)).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, Color.white, shape_surf.get_rect())
        self.win.blit(shape_surf, (self.width, 0, self.width, self.height))
    
    def move_up(self):
        """Move view up when is zoom in."""
        if self.shift_y - self.shift_step <= 0:
            self.shift_y = 0
            return
        self.shift_y -= self.shift_step
    
    def move_down(self):
        """Move down when is zoom in."""
        relative_height = self.height // self.gap // self.zoom_scale
        if self.shift_y + relative_height >= self.height//self.gap - self.zoom_scale*self.gap:
            return
        self.shift_y += self.shift_step
    
    def move_left(self):
        """Move left when is zoom in."""
        if self.shift_x - self.shift_step <= 0:
            self.shift_x = 0
            return
        self.shift_x -= self.shift_step
    
    def move_right(self):
        """Move right when is zoom in."""
        relative_width = self.width // self.gap // self.zoom_scale
        if self.shift_x + relative_width >= (self.width)//self.gap - self.zoom_scale*self.gap:
            return
        self.shift_x += self.shift_step
