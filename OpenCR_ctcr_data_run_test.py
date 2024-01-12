import numpy as np
import pandas as pd
import time
from OpenCR_ctcr_tcp import OpenCR_CTCR_tcp
from Aurora_py3 import Aurora
from tqdm import tqdm, trange


TEST_NAME = 'spiral_learning_joint'
AB2J = [3,0,4,1,5,2]
J2AB = [1,3,5,0,2,4]

FILENAME = f'./test_traj/{TEST_NAME}.csv'
DATASET_NAME = f'./test_traj/{TEST_NAME}_joint.csv'
df = pd.read_csv(FILENAME)
# add empty columns
df['actual_beta1'] = np.nan
df['actual_beta2'] = np.nan
df['actual_beta3'] = np.nan
df['actual_alpha1'] = np.nan
df['actual_alpha2'] = np.nan
df['actual_alpha3'] = np.nan
df['timestamp'] = np.nan

starting_index = 0
N_sample = df.shape[0]
## set up connection to CTCR
ctcr = OpenCR_CTCR_tcp(8111)

# manually put ctcr in starting position and pause
ctcr.go_to_target_slowly(target=ctcr.joint2encoder(df.iloc[starting_index, 0:6].to_numpy()))
time.sleep(1)

pbar = tqdm(total=N_sample)
print("starting data collection")
pbar.update(starting_index)
for i in range(starting_index+1, N_sample):
    ctcr.set_encoder_value_from_joint(df.iloc[starting_index + i, 0:6].to_numpy())
    time.sleep(0.05)
    actual_joint_values = ctcr.get_joint_values()
   
    df.iloc[starting_index + i, 6:12] = actual_joint_values[J2AB]
    df.iloc[starting_index + i, 12] = time.time()
    
    pbar.update(1)
pbar.close()
df.to_csv(DATASET_NAME+".csv", index=False)
