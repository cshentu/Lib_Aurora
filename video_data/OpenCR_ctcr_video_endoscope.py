# record frames from USB camera

import cv2
import numpy as np
import time

cap = cv2.VideoCapture("/dev/video6") # sometimes it's "/dev/video2"
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

time.sleep(2)
print("starting recording")
for i in range(4000):
    ret, frame = cap.read()
    # save to video subfolder
    cv2.imwrite("./video_data/video_sept12/"+str(time.time())+".png", frame)
    # time.sleep(0.05)
cap.release()
cv2.destroyAllWindows()
