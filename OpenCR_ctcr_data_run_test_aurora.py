import numpy as np
import pandas as pd
import time
from OpenCR_ctcr_tcp import OpenCR_CTCR_tcp
from Aurora_py3 import Aurora
from tqdm import tqdm, trange


TEST_NAME = 'circle_physics_joint'
AB2J = [3,0,4,1,5,2]
J2AB = [1,3,5,0,2,4]

FILENAME = f'./test_traj/{TEST_NAME}.csv'
DATASET_NAME = f'./test_traj/{TEST_NAME}_aurora.csv'
df = pd.read_csv(FILENAME)
# add empty columns
df['x1'] = np.nan
df['y1'] = np.nan
df['z1'] = np.nan
df['timestamp'] = np.nan

starting_index = 0
N_sample = df.shape[0]


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

pbar = tqdm(total=N_sample)
print("starting data collection")
pbar.update(starting_index)
for i in range(starting_index, N_sample):
    tracker.sensorData_collectData(n_times=1, starting_sensor=0)
    df.iloc[7] = tracker._port_handles[0]._trans[0]
    df.iloc[8] = tracker._port_handles[0]._trans[1]
    df.iloc[9] = tracker._port_handles[0]._trans[2]
    df.iloc[10] = time.time()
    pbar.update(1)
pbar.close()
df.to_csv(DATASET_NAME+".csv", index=False)

tracker._BEEP(2)
tracker.trackingStop()
# Close and disconnect Aurora
print('------------------------ closing ------------------------')
if tracker._isConnected:
    print('Nach dem Beep wird Aurora geschlossen')
    tracker._BEEP(1)
    tracker.disconnect()