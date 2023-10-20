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
DATASET_NAME = f'./test_traj/{TEST_NAME}_{time.time()}.csv'
df = pd.read_csv(FILENAME)
# add empty columns
df['actual_beta1'] = np.nan
df['actual_beta2'] = np.nan
df['actual_beta3'] = np.nan
df['actual_alpha1'] = np.nan
df['actual_alpha2'] = np.nan
df['actual_alpha3'] = np.nan

df['x1'] = np.nan
df['y1'] = np.nan
df['z1'] = np.nan
df['q01'] = np.nan
df['qx1'] = np.nan
df['qy1'] = np.nan
df['qz1'] = np.nan
df['error1'] = np.nan

df['x2'] = np.nan
df['y2'] = np.nan
df['z2'] = np.nan
df['q02'] = np.nan
df['qx2'] = np.nan
df['qy2'] = np.nan
df['qz2'] = np.nan
df['error2'] = np.nan

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
# assert tracker._n_port_handles==2, f"Number of Aurora sensors detected is not 2, got {tracker._n_port_handles}"
tracker.sensorData_collectData(n_times=10)

## set up connection to CTCR
ctcr = OpenCR_CTCR_tcp(8107)

# manually put ctcr in starting position and pause
ctcr.go_to_target_slowly(target=ctcr.joint2encoder(df.iloc[starting_index, 0:6].to_numpy()))
time.sleep(1.0)
tracker.sensorData_collectData(n_times=10)
for n in range(tracker._n_port_handles):
        df.iloc[0, 12 + n*8] = tracker._port_handles[n]._trans[0]
        df.iloc[0, 13 + n*8] = tracker._port_handles[n]._trans[1]
        df.iloc[0, 14 + n*8] = tracker._port_handles[n]._trans[2]
        df.iloc[0, 15 + n*8] = tracker._port_handles[n]._quaternion[0]
        df.iloc[0, 16 + n*8] = tracker._port_handles[n]._quaternion[1]
        df.iloc[0, 17 + n*8] = tracker._port_handles[n]._quaternion[2]
        df.iloc[0, 18 + n*8] = tracker._port_handles[n]._quaternion[3]
        df.iloc[0, 19 + n*8] = tracker._port_handles[n]._error

pbar = tqdm(total=N_sample)
print("starting data collection")
pbar.update(starting_index)
for i in range(starting_index+1, N_sample):
    ctcr.set_encoder_value_from_joint(df.iloc[starting_index + i, 0:6].to_numpy())
    time.sleep(0.05)
    actual_joint_values = ctcr.get_joint_values()
    # print('-'*30)
    # print("JOINT: ", actual_joint_values)
    df.iloc[starting_index + i, 6:12] = actual_joint_values[J2AB]
    # tracker.sensorData_collectData(n_times=1, starting_sensor=0)
    # for n in range(0,1): # only position sensor
    #     df.iloc[starting_index + i, 12 + n*8] = tracker._port_handles[n]._trans[0]
    #     df.iloc[starting_index + i, 13 + n*8] = tracker._port_handles[n]._trans[1]
    #     df.iloc[starting_index + i, 14 + n*8] = tracker._port_handles[n]._trans[2]
    #     df.iloc[starting_index + i, 15 + n*8] = tracker._port_handles[n]._quaternion[0]
    #     df.iloc[starting_index + i, 16 + n*8] = tracker._port_handles[n]._quaternion[1]
    #     df.iloc[starting_index + i, 17 + n*8] = tracker._port_handles[n]._quaternion[2]
    #     df.iloc[starting_index + i, 18 + n*8] = tracker._port_handles[n]._quaternion[3]
    #     df.iloc[starting_index + i, 19 + n*8] = tracker._port_handles[n]._error
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