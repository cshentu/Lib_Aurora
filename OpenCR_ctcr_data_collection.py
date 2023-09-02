import numpy as np
import pandas as pd
import time
from OpenCR_CTCR_tcp import OpenCR_CTCR_tcp
from Aurora_py3 import Aurora

FIELNAME = 'beta_alpha_joint_values.csv'
INDEXING = [3,0,4,1,5,2]
INDEXING_ACTUAL = [9,6,10,7,11,8]
DATASET_NAME = 'beta_alpha_joint_values_dataset.csv'
df = pd.read_csv(FIELNAME)
# add empty columns
df['actual_beta1'] = np.nan
df['actual_beta2'] = np.nan
df['actual_beta3'] = np.nan
df['actual_alpha1'] = np.nan
df['actual_alpha2'] = np.nan
df['actual_alpha3'] = np.nan
df['x'] = np.nan
df['y'] = np.nan
df['z'] = np.nan

starting_index = 0
N_sample = 10

## set up connection to Aurora
tracker = Aurora(baud_rat=9600)
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

## set up connection to CTCR
ctcr = OpenCR_CTCR_tcp(8083)


for i in range(0, N_sample):
    ctcr.set_joint_values(df.iloc[starting_index + i, INDEXING])
    time.sleep(2)
    actual_joint_values = ctcr.get_joint_values()
    df.iloc[starting_index + i, INDEXING_ACTUAL] = actual_joint_values

    for n in range(10):
        tracker.sensorData_updateAll()
        tracker.sensorData_write(n)
    df.iloc[starting_index + i, 12] = tracker._port_handles[n]._trans[0]
    df.iloc[starting_index + i, 13] = tracker._port_handles[n]._trans[1]
    df.iloc[starting_index + i, 14] = tracker._port_handles[n]._trans[2]
    df.to_csv(DATASET_NAME, index=False)