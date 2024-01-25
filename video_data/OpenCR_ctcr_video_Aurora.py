import numpy as np
import pandas as pd
import time
from OpenCR_ctcr_tcp import OpenCR_CTCR_tcp
from Aurora_py3 import Aurora
from tqdm import tqdm, trange

FILENAME = 'joint_values_video.csv'

AB2J = [3,0,4,1,5,2]
J2AB = [1,3,5,0,2,4]

DATASET_NAME = 'video_aurora_jan25' 
df = pd.read_csv(FILENAME)

####################
# Assuming two aurora sensors, one on the base and one on the end effector
# The base aurora sensor has a lower port number
####################


## set up connection to Aurora
tracker = Aurora(baud_rat=921600)
if not tracker._isConnected:
    print('tracker is not connected!')
    tracker.connect()

time.sleep(.1)
if tracker._isConnected:
    print('tracker is connected!')

time.sleep(.1)
tracker.init()
print('tracker._serial_object.isOpen() is ' + str(tracker._serial_object.isOpen()))
print('tracker._device_init is ' + str(tracker._device_init))

print('------------------------ setting ------------------------')
time.sleep(0.1)
tracker.portHandles_detectAndAssign_FlowChart(printFeedback=True)
time.sleep(0.1)
tracker.portHandles_updateStatusAll()
print('------------------------ tracking ------------------------')
tracker.trackingStart()
time.sleep(2)
assert tracker._n_port_handles==2, f"Number of Aurora sensors detected is not 2, got {tracker._n_port_handles}"
tracker.sensorData_collectData(n_times=10)

# store initial base position
df.iloc[0, 0] = "base"
df.iloc[0, 1] = time.time()
df.iloc[0, 2] = tracker._port_handles[0]._trans[0]
df.iloc[0, 3] = tracker._port_handles[0]._trans[1]
df.iloc[0, 4] = tracker._port_handles[0]._trans[2]
df.iloc[0, 5] = tracker._port_handles[0]._quaternion[0]
df.iloc[0, 6] = tracker._port_handles[0]._quaternion[1]
df.iloc[0, 7] = tracker._port_handles[0]._quaternion[2]
df.iloc[0, 8] = tracker._port_handles[0]._quaternion[3]

# continously update end effector position
df_idx = 1
try:
    while True:
        pose = tracker.sensorData_collect1sensor(1)
        df.iloc[df_idx, 0] = "tip"
        df.iloc[df_idx, 1] = time.time()
        df.iloc[df_idx, 2:9] = pose
        df_idx += 1
except KeyboardInterrupt:
    print('Ending collection, saving data!')
    df.to_csv(DATASET_NAME+".csv", index=False)
    tracker._BEEP(2)
    tracker.trackingStop()
    # Close and disconnect Aurora
    print('------------------------ closing ------------------------')
    if tracker._isConnected:
        print('Nach dem Beep wird Aurora geschlossen')
        tracker._BEEP(1)
        tracker.disconnect()

