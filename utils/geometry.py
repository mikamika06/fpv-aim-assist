import math 

def box_center(x1, y1, x2, y2):
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    return x_center, y_center

def box_area(x1, y1, x2, y2):
    return (x2 - x1) * (y2 - y1)

def frame_center(frame):
    h, w, _ = frame.shape
    return w / 2, h / 2

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def clamp(value, min_value=-1.0, max_value=1.0):
    return max(min_value, min(max_value, value))

