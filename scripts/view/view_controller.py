import pygame
from model.model import Model
from utils.enums import ViewType
from view.button import Button
from view.spot import Spot
from view.button_handler import ButtonHandler
from view.colors import Color
from view.view_params import View


class ViewController:
    def __init__(self) -> None:
        View.window = pygame.display.set_mode((View.width + 220, View.height))
        pygame.display.set_caption("Fire figters vs fire")
        View.window.fill(Color.white)
        self.view_type = ViewType.MAP
        self.max_zoom_scale = 8
        self.min_zoom_scale = 1
        self.shift_step = 10  # how many cells to shiht when moving

    def draw_model(self, model: Model, iteration):
        """Draws square grid with colored spots."""
        for y in range(View.shift_y, len(model.grid)):
            for x in range(View.shift_x, len(model.grid[0])):
                model.grid[y][x].visual.draw()
        self.draw_panel()
        if self.view_type == ViewType.FIRE_FIGHTERS:
            self.draw_fog()
            for team in model.teams:
                self.draw_fighters(team)

        self.draw_compass()
        self.draw_controls_legend()
        self.draw_timer(iteration)

    def draw_fighters(self, team):
        for fighter in team.fighters:
            fighter.draw()
        smallfont = pygame.font.SysFont('Verdana', 9 + int(View.gap*2.5))
        text = smallfont.render(str(team.team_id), True, Color.white)
        View.window.blit(text, ((
            team.target_sector[1] * 10 - View.shift_x) * View.gap * View.zoom_scale + 4, (team.target_sector[0] * 10 - View.shift_y) * View.gap * View.zoom_scale + 4))

    def draw_fog(self):
        """Add a layer of gray fog to enable fire figthers more cleaner visualization."""
        shape_surf = pygame.Surface(pygame.Rect(
            (0, 0, View.width, View.width)).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, Color.fog, shape_surf.get_rect())
        View.window.blit(shape_surf, (0, 0, View.width, View.width))

    def draw_buttons(self, button_handler: ButtonHandler):
        """Draws all buttons from list."""
        for button in button_handler.buttons:
            button.draw()
        self.draw_compass()

    def draw_compass(self):
        """Draw compass image."""
        imp = pygame.image.load(
            "scripts\img\compass_small.png").convert_alpha()
        View.window.blit(imp, (View.width + 35, View.height - 190))

    def draw_controls_legend(self):
        """Draw controls legend image."""
        imp = pygame.image.load(
            "scripts\img\controls.png").convert_alpha()
        View.window.blit(imp, (View.width + 15, 20))

    def draw_timer(self, iteration):
        """Draw timer above the compass."""
        imp = pygame.image.load(
            "scripts\img\\frame.png").convert_alpha()
        View.window.blit(imp, (View.width + 15, View.height - 290))
        pygame.draw.rect(View.window, Color.white, [
            View.width + 25, View.height - 280, 180, 20])
        smallfont = pygame.font.SysFont('Verdana', 16)
        text = smallfont.render("{:.2f}".format(
            iteration / 15) + " min", True, Color.black)  # 360 it -> 12 min
        View.window.blit(text, (View.width + 35, View.height - 280))

    def update(self):
        pygame.display.update()
        
    def save_image(self, iteration, path):
        pygame.image.save(View.window, f"{path}_{str(iteration).zfill(5)}.png")

    def get_clicked_pos(self, pos) -> tuple():
        """Returns row and columns idx of clicked place."""
        x, y = pos
        row = y // View.gap // View.zoom_scale + View.shift_y
        col = x // View.gap // View.zoom_scale + View.shift_x
        return row, col

    def zoom_in(self):
        """Zoom in the view with factor = 2. Max and zoom scales are defined in constructor."""
        if View.zoom_scale < self.max_zoom_scale:
            View.zoom_scale = int(2*View.zoom_scale)
            Spot.zoom = View.zoom_scale

    def zoom_out(self):
        """Zoom out the view with factor = 2. Max and zoom scales are defined in constructor."""
        if View.zoom_scale > 1:
            View.zoom_scale = int(View.zoom_scale//2)

        relative_height = View.height // View.gap // View.zoom_scale
        if View.shift_y + relative_height >= View.height//View.gap - View.zoom_scale*2:
            View.shift_y = View.height//View.gap - View.zoom_scale*2 - relative_height

        relative_width = View.width // View.gap // View.zoom_scale
        if View.shift_x + relative_width >= (View.width)//View.gap - View.zoom_scale*2:
            View.shift_x = (View.width)//View.gap - \
                View.zoom_scale*2 - relative_width

        if View.zoom_scale == 1:
            View.shift_x = 0
            View.shift_y = 0

    def draw_panel(self):
        """Draw panel with includes timer, compass and legend."""
        shape_surf = pygame.Surface(pygame.Rect(
            (0, 0, 220, View.height)).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, Color.white, shape_surf.get_rect())
        View.window.blit(shape_surf, (View.width, 0, View.width, View.height))

    def move_up(self):
        """Move view up when is zoom in."""
        if View.shift_y - self.shift_step <= 0:
            View.shift_y = 0
            return
        View.shift_y -= self.shift_step

    def move_down(self):
        """Move down when is zoom in."""
        relative_height = View.height // View.gap // View.zoom_scale
        if View.shift_y + relative_height >= View.height//View.gap - View.zoom_scale*View.gap:
            return
        View.shift_y += self.shift_step

    def move_left(self):
        """Move left when is zoom in."""
        if View.shift_x - self.shift_step <= 0:
            View.shift_x = 0
            return
        View.shift_x -= self.shift_step

    def move_right(self):
        """Move right when is zoom in."""
        relative_width = View.width // View.gap // View.zoom_scale
        if View.shift_x + relative_width >= (View.width)//View.gap - View.zoom_scale*View.gap:
            return
        View.shift_x += self.shift_step
