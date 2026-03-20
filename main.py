import time
import cv2

from config import (
    MODEL_PATH,
    TARGET_CLASS,
    CONF_THRESHOLD,
    WINDOW_NAME,
    SCREEN_MONITOR,
    DEAD_ZONE,
    MAX_MISSED_FRAMES,
    TRACKING_DISTANCE_THRESHOLD,
    KP_YAW,
    KD_YAW,
    KP_PITCH,
    KD_PITCH,
    MAX_YAW,
    MAX_PITCH,
    DETECT_EVERY_N_FRAME
)

from core.frame_source import ScreenSource
from core.detector import Detector
from core.target_selector import TargetSelector
from core.tracker import Tracker
from core.controller import Controller
from core.visualizer import Visualizer
from core.input_reader import InputReader
from core.mode_manager import ModeManager, FlightMode
from core.mixer import ControlMixer
from core.virtual_pad import VirtualPad
from utils.geometry import frame_center


def main():
    detector = Detector(MODEL_PATH)
    selector = TargetSelector(TARGET_CLASS, CONF_THRESHOLD)
    tracker = Tracker(
        max_missed_frames=MAX_MISSED_FRAMES,
        distance_threshold=TRACKING_DISTANCE_THRESHOLD
    )

    controller = Controller(
        dead_zone=DEAD_ZONE,
        kp_yaw=KP_YAW,
        kd_yaw=KD_YAW,
        kp_pitch=KP_PITCH,
        kd_pitch=KD_PITCH,
        max_yaw=MAX_YAW,
        max_pitch=MAX_PITCH,
    )

    visualizer = Visualizer()
    source = ScreenSource(SCREEN_MONITOR)

    input_reader = InputReader()
    mode_manager = ModeManager()
    mixer = ControlMixer(assist_gain=0.20)
    virtual_pad = VirtualPad()

    prev_error_x = None
    prev_error_y = None
    prev_time = None

    frame_index = 0
    last_candidates = []

    try:
        while True:
            frame_index += 1
            now = time.time()

            buttons, pilot_input = input_reader.read()
            mode = mode_manager.update(buttons, pilot_input)

            frame = source.read()
            if frame is None:
                print("Not found")
                break

            current_frame_center = frame_center(frame)

            if frame_index % DETECT_EVERY_N_FRAME == 0:
                detections = detector.detect(frame)
                last_candidates = selector.get_candidates(detections)

            target = tracker.update(last_candidates)

            assist_input = {
                "roll": 0.0,
                "pitch": 0.0,
                "yaw": 0.0,
                "throttle": 0.0,
            }

            if target is not None:
                error_x = target["center"][0] - current_frame_center[0]
                error_y = target["center"][1] - current_frame_center[1]

                if prev_time is None:
                    dt = 0.0
                else:
                    dt = now - prev_time

                if dt > 1e-6 and prev_error_x is not None and prev_error_y is not None:
                    error_x_rate = (error_x - prev_error_x) / dt
                    error_y_rate = (error_y - prev_error_y) / dt
                else:
                    error_x_rate = 0.0
                    error_y_rate = 0.0

                state = {
                    "error_x": error_x,
                    "error_y": error_y,
                    "error_x_rate": error_x_rate,
                    "error_y_rate": error_y_rate,
                    "frame_center_x": current_frame_center[0],
                    "frame_center_y": current_frame_center[1],
                }

                control = controller.compute(state)

                assist_input = {
                    "roll": 0.0,
                    "pitch": control["pitch"],
                    "yaw": control["yaw"],
                    "throttle": 0.0,
                }

                prev_error_x = error_x
                prev_error_y = error_y
                prev_time = now

                visualizer.draw_target(frame, target)
            else:
                tracker.reset()
                controller.reset()

                prev_error_x = None
                prev_error_y = None
                prev_time = None

                visualizer.draw_no_target(frame)

            if mode == FlightMode.MANUAL:
                output = mixer.mix_manual(pilot_input)
                mode_text = "MANUAL"
            else:
                output = mixer.mix_assist(pilot_input, assist_input)
                mode_text = "ASSIST"

            virtual_pad.apply(output)

            visualizer.draw_frame_center(frame, current_frame_center)
            visualizer.draw_mode(frame, mode_text)

            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1)
            if key == 27:
                break

    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        virtual_pad.reset()
        source.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()