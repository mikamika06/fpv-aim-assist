from utils.geometry import clamp

class Controller:
    def __init__(
        self,
        dead_zone,
        kp_yaw, kd_yaw,
        kp_pitch, kd_pitch,
        max_yaw, max_pitch,
    ):
        self.dead_zone_px = dead_zone

        self.kp_yaw = kp_yaw
        self.kd_yaw = kd_yaw

        self.kp_pitch = kp_pitch
        self.kd_pitch = kd_pitch

        self.max_yaw = max_yaw
        self.max_pitch = max_pitch

    def compute(self, state):
        error_x = state["error_x"]
        error_y = state["error_y"]
        error_x_rate = state["error_x_rate"]
        error_y_rate = state["error_y_rate"]
        frame_center_x = state["frame_center_x"]
        frame_center_y = state["frame_center_y"]

        if abs(error_x) < self.dead_zone_px:
            error_x = 0.0

        if abs(error_y) < self.dead_zone_px:
            error_y = 0.0

        norm_error_x = error_x / frame_center_x
        norm_error_y = error_y / frame_center_y

        norm_error_x_rate = error_x_rate / frame_center_x
        norm_error_y_rate = error_y_rate / frame_center_y
        yaw = self.kp_yaw * norm_error_x + self.kd_yaw * norm_error_x_rate
        pitch = self.kp_pitch * norm_error_y + self.kd_pitch * norm_error_y_rate

        yaw = clamp(yaw, -self.max_yaw, self.max_yaw)
        pitch = clamp(pitch, -self.max_pitch, self.max_pitch)

        return {
            "pitch": pitch,
            "yaw": yaw,
        }

    def reset(self):
        pass