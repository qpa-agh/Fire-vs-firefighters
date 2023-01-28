import pygame
from view.colors import Color
from view.view_params import View


class Button:
    """Representation of button displayed next to the grid."""
    window = None

    def __init__(self, name, value, pos) -> None:
        self.size_y = 30
        self.size_x = 30
        self.start_x, self.start_y = pos
        self.text_start_x, self.text_start_y = pos
        self.name = name
        self.value = value
        self.color = Color.button
        self.compute_text_pos()

    def compute_text_pos(self):
        self.text_start_y -= 2
        self.text_start_x -= (1 + (3 * len(self.name)))
        if len(self.name) == 1:
            self.size_x = 14
        if "W" in self.name:
            self.text_start_x += 2

    def is_inside(self, x_pos, y_pos):
        """Checks if the point with given coefficients is within the button."""
        if x_pos < self.start_x or x_pos > self.start_x + self.size_x:
            return False
        if y_pos < self.start_y or y_pos > self.start_y + self.size_y:
            return False
        return True

    def draw(self):
        """Draws square button with its name."""
        pygame.draw.rect(View.window, self.color, [
                         self.text_start_x, self.text_start_y, self.size_x+10, self.size_y],  border_radius=10)
        # text
        smallfont = pygame.font.SysFont('Verdana', 16)
        text = smallfont.render(self.name, True, Color.black)
        View.window.blit(text, (self.start_x + 2, self.start_y + 2))

    def is_pushed(self):
        """Checks if button is pushed."""
        return self.color == Color.button_pushed

    def set_pushed(self):
        """Set button as pushed."""
        self.color = Color.button_pushed

    def set_not_pushed(self):
        """Set button as not pushed."""
        self.color = Color.button

    def get_value(self):
        return self.value
