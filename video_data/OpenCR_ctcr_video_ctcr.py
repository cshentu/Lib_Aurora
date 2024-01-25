import numpy as np
import pandas as pd
import time
from OpenCR_ctcr_tcp import OpenCR_CTCR_tcp
from tqdm import tqdm, trange

FILENAME = 'joint_values_video.csv'

AB2J = [3,0,4,1,5,2]
J2AB = [1,3,5,0,2,4]

DATASET_NAME = 'video_ctcr_jan25' 
df = pd.read_csv(FILENAME)

starting_index = 0
N_sample = 20000


## set up connection to CTCR
ctcr = OpenCR_CTCR_tcp(8211)

# manually put ctcr in retracted position
ctcr.go_to_target_slowly(target=np.array([0, 14, 0, 20, 0, 30]))
time.sleep(2.0)


pbar = tqdm(total=N_sample)
print("starting robot")
pbar.update(starting_index)
for i in range(starting_index, N_sample):
    ctcr.set_joint_values(df.iloc[starting_index + i, 0:6].to_numpy()[AB2J])
    ctcr.go_to_target_slowly(n_steps=15, target=df.iloc[starting_index + i, 0:6].to_numpy()[AB2J])
    # print(df.iloc[starting_index + i, 0:6].to_numpy())
    time.sleep(0.1)
    actual_joint_values = ctcr.get_joint_values()
    # print('-'*30)
    # print("JOINT: ", actual_joint_values)
    df.iloc[starting_index + i, 6:12] = actual_joint_values[J2AB]

    pbar.update(1)
pbar.close()
df.to_csv(DATASET_NAME+".csv", index=False)
