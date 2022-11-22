import pygame
from view.colors import Color


class Button:
    """Representation of button displayed next to the grid."""

    def __init__(self, name, value, start_x, start_y) -> None:
        self.size_y = 30
        self.size_x = 80
        self.start_y = start_y
        self.start_x = start_x
        self.name = name
        self.value = value
        self.color = Color.button

    def is_inside(self, x_pos, y_pos):
        """Checks if the point with given coefficients is within the button."""
        if x_pos < self.start_x or x_pos > self.start_x + self.size_x:
            return False
        if y_pos < self.start_y or y_pos > self.start_y + self.size_y:
            return False
        return True

    def draw(self, win):
        """Draws square button with its name."""
        pygame.draw.rect(win, self.color, [
                         self.start_x, self.start_y, self.size_x, self.size_y])

        # text
        smallfont = pygame.font.SysFont('Verdana', 16)
        text = smallfont.render(self.name, True, Color.black)
        win.blit(text, (self.start_x + 12, self.start_y + 5))

    def is_pushed(self):
        """Checks if button is pushed."""
        return self.color == Color.button_pushed

    def set_pushed(self):
        """Set button as pushed."""
        self.color = Color.button_pushed

    def set_not_pushed(self):
        """Set button as not pushed."""
        self.color = Color.button

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value
