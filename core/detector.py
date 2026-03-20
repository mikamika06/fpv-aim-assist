from ultralytics import YOLO
from utils.geometry import box_center, box_area

class Detector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
    
    def detect(self, frame):
        results = self.model(frame, verbose=False)
        boxes = results[0].boxes

        detections = []

        for box in boxes:
            cls_id = int(box.cls[0])
            class_name = self.model.names[cls_id]
            conf = float(box.conf[0])

            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)

            center = box_center(x1, y1, x2, y2)
            area = box_area(x1, y1, x2, y2)

            detections.append({
                "class_name": class_name,
                "conf": conf,
                "box": (x1, y1, x2, y2),
                "center": center,
                "area": area,
            })
        return detections