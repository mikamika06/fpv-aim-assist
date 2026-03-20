class TargetSelector:
    def __init__(self, target_class, conf_threshold):
        self.target_class = target_class
        self.conf_threshold = conf_threshold
    
    def get_candidates(self, detections):
        candidates = []

        for det in detections:
            if det["class_name"] != self.target_class:
                continue

            if det["conf"] < self.conf_threshold:
                continue

            candidates.append(det)

        return candidates