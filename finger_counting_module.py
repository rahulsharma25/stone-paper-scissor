import cv2 as cv
import mediapipe as mp
import time
import numpy as np
import hand_tracking_module as htm

class Finger_counter():
    def __init__(self, min_detection_con=0.5, draw_hand=True):
        self.min_detection_con = min_detection_con
        self.draw_hand = draw_hand
        self.finger_tip_ids = [4, 8, 12, 16, 20]
        self.detector = htm.Hand_detector(detection_confidence = self.min_detection_con)

    def count_fingers(self, img):
        img = self.detector.find_hands(img, draw=self.draw_hand)
        lm_list = self.detector.find_position(img, draw=False)

        finger_open_status = []

        if len(lm_list) != 0:
            if lm_list[self.finger_tip_ids[0]][1] > lm_list[self.finger_tip_ids[0]-1][1]:
                finger_open_status.append(1)
            else:
                finger_open_status.append(0)
            
            for i in range(1, 5):
                if lm_list[self.finger_tip_ids[i]][2] < lm_list[self.finger_tip_ids[i]-2][2]:
                    finger_open_status.append(1)
                else:
                    finger_open_status.append(0)
        
        return finger_open_status, finger_open_status.count(1)

def main():
    cap = cv.VideoCapture(0)

    p_time = 0
    while True:
        isTrue, img = cap.read()

        c_time = time.time()
        fps = 1/(c_time - p_time)
        p_time = c_time
        cv.putText(img, str(int(fps)), (10, 30), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv.imshow("Video", img)

        if cv.waitKey(1) == ord('q'):
            break

if __name__ == "__main__":
    main()