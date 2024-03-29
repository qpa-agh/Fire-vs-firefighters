from view.button import Button
import time


class ButtonHandler:
    """Manages all buttons and guarantees that exacly one button is pushed."""

    def __init__(self, button_names_and_values) -> None:
        self.buttons = self.createButtons(button_names_and_values)

    def createButtons(self, button_names_and_values):
        buttons = []
        for name, value, pos in button_names_and_values:
            buttons.append(Button(name, value, pos))
        return buttons

    def click_proper_button(self, x_pos, y_pos):
        """Sets button as pushed if given coefficients are within the button."""
        for button in self.buttons:
            button.set_not_pushed()
        for button in self.buttons:
            if button.is_inside(x_pos, y_pos):
                button.set_pushed()
                return button.get_value()
        return None