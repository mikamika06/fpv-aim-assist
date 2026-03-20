from utils.geometry import clamp

# def clamp(v, lo=-1.0, hi=1.0):
#     return max(lo, min(hi, v))

class ControlMixer:
    def __init__(self, assist_gain=0.35):
        self.assist_gain = assist_gain
        self.throttle_assist_gain = 0.30  

    def mix_manual(self, pilot_input):
        return {
            "roll": clamp(pilot_input["roll"]),
            "pitch": clamp(pilot_input["pitch"]),
            "yaw": clamp(pilot_input["yaw"]),
            "throttle": clamp(pilot_input["throttle"]),
        }

    def mix_assist(self, pilot_input, assist_input):
        return {
            "roll": clamp(pilot_input["roll"] + self.assist_gain * assist_input.get("roll", 0.0)),
            "pitch": clamp(pilot_input["pitch"] + self.assist_gain * assist_input.get("pitch", 0.0)),
            "yaw": clamp(pilot_input["yaw"] + self.assist_gain * assist_input.get("yaw", 0.0)),
            "throttle": clamp(pilot_input["throttle"] + self.throttle_assist_gain * assist_input.get("throttle", 0.0)),
        }