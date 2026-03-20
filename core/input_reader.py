import pygame

class InputReader:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            raise RuntimeError("Gamepad not found")

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.prev_buttons = {}

    def _get_button_edge(self, name, current_value):
        prev_value = self.prev_buttons.get(name, False)
        self.prev_buttons[name] = current_value
        return current_value and not prev_value

    def read(self):
        pygame.event.pump()

        lx = self.joystick.get_axis(0)
        ly = self.joystick.get_axis(1)
        rx = self.joystick.get_axis(2)
        ry = self.joystick.get_axis(3)

        sticks = {
            "yaw": float(lx),
            "pitch": float(-ry),
            "roll": float(rx),
            "throttle": float(-ly),
        }

        r3 = bool(self.joystick.get_button(8))
        r2 = bool(self.joystick.get_button(7))

        buttons = {
            "assist_toggle": self._get_button_edge("assist_toggle", r3)
        }

        return buttons, sticks