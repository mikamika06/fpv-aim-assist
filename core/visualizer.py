import cv2


class Visualizer:
    def draw_target(self, frame, target):
        x1, y1, x2, y2 = target["box"]
        x_center, y_center = target["center"]
        conf = target["conf"]
        class_name = target["class_name"]

        cv2.rectangle(
            frame,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0, 255, 0),
            2
        )

        cv2.circle(
            frame,
            (int(x_center), int(y_center)),
            6,
            (0, 255, 0),
            -1
        )

        text_y = max(25, int(y1) - 10)

        cv2.putText(
            frame,
            f"{class_name} {conf:.2f}",
            (int(x1), text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

    def draw_no_target(self, frame):
        cv2.putText(
            frame,
            "NO TARGET",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
            cv2.LINE_AA
        )

    def draw_frame_center(self, frame, frame_center):
        frame_center_x, frame_center_y = frame_center

        cv2.circle(
            frame,
            (int(frame_center_x), int(frame_center_y)),
            6,
            (0, 0, 255),
            -1
        )

    def draw_mode(self, frame, mode_text):
        cv2.putText(
            frame,
            f"MODE: {mode_text}",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

    def draw_info(self, frame, control_data):
        cv2.putText(
            frame,
            f"error_x: {int(control_data['error_x'])} {control_data['command_x']}",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        cv2.putText(
            frame,
            f"error_y: {int(control_data['error_y'])} {control_data['command_y']}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )