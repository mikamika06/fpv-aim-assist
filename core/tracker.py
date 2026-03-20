from utils.geometry import distance

class Tracker:
    def __init__(self, max_missed_frames=10, distance_threshold=180):
        self.prev_target = None
        self.missed_frames = 0
        self.max_missed_frames = max_missed_frames
        self.distance_threshold = distance_threshold

    def update(self, candidates):
        if not candidates:
            self.missed_frames += 1
            if self.missed_frames > self.max_missed_frames:
                self.prev_target = None
            return self.prev_target

        if self.prev_target is None:
            best_target = max(candidates, key=lambda det: det["area"])
            self.prev_target = best_target
            self.missed_frames = 0
            return best_target

        prev_center = self.prev_target["center"]

        nearest = min(
            candidates,
            key=lambda det: distance(det["center"], prev_center)
        )

        dist = distance(nearest["center"], prev_center)

        if dist > self.distance_threshold:
            best_target = max(candidates, key=lambda det: det["area"])
            self.prev_target = best_target
            self.missed_frames = 0
            return best_target

        self.prev_target = nearest
        self.missed_frames = 0
        return nearest

    def reset(self):
        self.prev_target = None
        self.missed_frames = 0