import pygame
from colors import Color
from typing import List


class Button:
    """Representation of button displayed next to the grid."""

    def __init__(self, name, start_x, start_y) -> None:
        self.size_x = 30
        self.size_y = 80
        self.start_x = start_x
        self.start_y = start_y
        self.name = name
        self.color = Color.button

    def is_inside(self, y_pos, x_pos):
        """Checks if the point with given coefficients is within the button."""
        if x_pos < self.start_x or x_pos > self.start_x + self.size_y:
            return False
        if y_pos < self.start_y or y_pos > self.start_y + self.size_x:
            return False
        return True

    def draw(self, win):
        """Draws square button with its name."""
        pygame.init()
        pygame.draw.rect(win, self.color, [
                         self.start_x, self.start_y, self.size_y, self.size_x])

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


class ButtonHandler:
    """Manages all buttons and guarantees that exacly one button is pushed."""

    def __init__(self, button_names, start: int) -> None:
        self.start_x = start
        self.buttons = self.createButtons(button_names)
    
    def createButtons(self, button_names):
        padding = 50
        buttons = []
        for name in button_names:
            button = Button(name, self.start_x, padding)
            padding += 50
            buttons.append(button)
        return buttons

    def draw_all_buttons(self, win):
        """Draws all buttons from list."""
        for button in self.buttons:
            button.draw(win)

    def click_proper_button(self, x_pos, y_pos):
        """Sets button as pushed if given coefficients are within the button."""
        for button in self.buttons:
            if button.is_inside(x_pos, y_pos):
                for other_button in self.buttons:
                    other_button.set_not_pushed()
                button.set_pushed()
                return button.get_name()
        return None
