# record frames from USB camera

import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

time.sleep(2)
print("starting recording")
for i in range(10):
    ret, frame = cap.read()
    # save to video subfolder
    cv2.imwrite("video_data/video/"+str(time.time())+".png", frame)
    time.sleep(0.05)
cap.release()
cv2.destroyAllWindows()
