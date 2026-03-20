import vgamepad as vg
from utils.geometry import clamp

def to_short_axis(value):
    value = clamp(value)
    return int(value * 32767)


def to_trigger(value):
    value = clamp((value + 1.0) / 2.0, 0.0, 1.0)
    return int(value * 255)


class VirtualPad:
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()

    def apply(self, controls):
        roll = clamp(controls["roll"])
        pitch = clamp(controls["pitch"])
        yaw = clamp(controls["yaw"])
        throttle = clamp(controls["throttle"])

        self.gamepad.left_joystick(
            x_value=to_short_axis(yaw),
            y_value=to_short_axis(-throttle)
        )

        self.gamepad.right_joystick(
            x_value=to_short_axis(roll),
            y_value=to_short_axis(-pitch)
        )

        self.gamepad.update()

    def reset(self):
        self.gamepad.reset()
        self.gamepad.update()