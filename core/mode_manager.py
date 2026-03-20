from enum import Enum, auto


class FlightMode(Enum):
    MANUAL = auto()
    ASSIST = auto()


class ModeManager:
    def __init__(self):
        self.mode = FlightMode.MANUAL

    def update(self, buttons, sticks):

        if buttons.get("assist_toggle", False):
            if self.mode == FlightMode.MANUAL:
                self.mode = FlightMode.ASSIST
            else:
                self.mode = FlightMode.MANUAL

        manual_override_threshold = 0.75

        if self.mode == FlightMode.ASSIST:
            if (
                abs(sticks.get("roll", 0.0)) > manual_override_threshold or
                abs(sticks.get("pitch", 0.0)) > manual_override_threshold or
                abs(sticks.get("yaw", 0.0)) > manual_override_threshold
            ):
                self.mode = FlightMode.MANUAL

        return self.mode