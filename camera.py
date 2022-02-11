import cv2 as cv
import mediapipe as mp
import hand_tracking_module as htm
import finger_counting_module as fcm
import time
import numpy as np

def play_game(open_fingers_count, img):
    moves = ["STONE", "PAPER", "SCISSOR"]

    com_move = np.random.randint(0, 3)

    my_move = 0
    if open_fingers_count == 5:
        my_move = 1
    if open_fingers_count == 2:
        my_move = 2    
    
    cv.putText(img, f"COM Chose: {moves[com_move]}", (10, 90), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
    cv.putText(img, f"YOU Chose: {moves[my_move]}", (10, 120), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

    statuses = ["LOSE", "DRAW", "WIN"]
    status = 0
    if com_move == my_move:
        status = 1
    else:
        if com_move == 0:
            if my_move == 1:
                status = 2
            else:
                status = 0

        elif com_move == 1:
            if my_move == 0:
                status = 0
            else:
                status = 2

        else:
            if my_move == 0:
                status = 2
            else:
                status = 0
    
    cv.putText(img, f"RESULT: {statuses[status]}", (10, 150), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
    return img, moves[com_move], moves[my_move], statuses[status]


class Camera():
    def __init__(self, min_detection_con = 0.5):
        self.cap = cv.VideoCapture(0)
        self.finger_counter = fcm.Finger_counter(min_detection_con=min_detection_con, draw_hand=True)
        self.flag_time = time.time()
        self.time_remaining = 5
        self.played_one = False
        self.prev_com_move = 0
        self.prev_my_move = 0
        self.prev_res = 0

    def get_frame(self):
        isTrue, img = self.cap.read()
        
        _, open_fingers_count = self.finger_counter.count_fingers(img)
        cv.putText(img, f"TIME REMAINING: {self.time_remaining}", (10, 60), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        if self.played_one:
            cv.putText(img, f"COM Chose: {self.prev_com_move}", (10, 90), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
            cv.putText(img, f"YOU Chose: {self.prev_my_move}", (10, 120), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
            cv.putText(img, f"RESULT: {self.prev_res}", (10, 150), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

        if self.time_remaining == 0:
            img, self.prev_com_move, self.prev_my_move, self.prev_res = play_game(open_fingers_count, img)
            self.played_one = True
            self.time_remaining = 5

        c_time = time.time()
        if c_time-self.flag_time >= 1:
            self.time_remaining -= 1
            self.flag_time = c_time

        return img

def main():
    cam = Camera(0.8)
    while True:
        img = cam.get_frame()
        cv.imshow("Video", img)

        if cv.waitKey(1) == ord('q'):
            break
    
    return

if __name__ == "__main__":
    main()