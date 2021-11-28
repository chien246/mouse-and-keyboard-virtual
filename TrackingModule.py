import cv2 as cv
import mediapipe as mp
from utils import get_index_fingers

class HandTracking:
    def __init__(
            self,
            mode = False,
            hand_number = 1,
            min_detection_confidence = 0.5,
            min_tracking_confidence = 0.5):
        self.mode = mode
        self.hand_number = hand_number
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(mode, hand_number, min_detection_confidence, min_tracking_confidence)
        self.draw_tool = mp.solutions.drawing_utils

    def findLandMark(self, image):
        imgRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        results = self.hands.process(imgRGB)

        landmarksList = results.multi_hand_landmarks
        if landmarksList:
            return list(landmarksList[0].landmark)

        return None

    def isRaiseFinger(self, landmarks, finger):
        point1, point2 = get_index_fingers(finger)

        if (landmarks[point1].y <= landmarks[point2].y):
            return True

        return False






