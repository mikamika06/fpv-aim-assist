import cv2
import numpy as np
import mss

class ScreenSource:
    def __init__(self, monitor):
        self.sct = mss.mss()
        self.monitor = monitor
    
    def read(self):
        screenshot = self.sct.grab(self.monitor)
        frame = np.array(screenshot)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame

    def release(self):
        self.sct.close()
    