import numpy as np
import pandas as pd

# generate random joint spaces points for recording video data
# -> less number of points + no ordering

np.random.seed(500) # v2
# np.random.seed(520)
# np.random.seed(250)
N_sample = 100
L1 = 17
L2 = 23
L3 = 34
MB = np.array([[-L1, 0, 0],
               [-L1, L1-L2, 0],
               [-L1, L1-L2, L2-L3],])

# Generate random joint values
beta_joint_values_01 = np.random.rand(3, N_sample)
beta_joint_values = - MB @ beta_joint_values_01
alpha_joint_values = (np.random.rand(3, N_sample) - 0.5) * 2 * np.pi/3 * 4

# create a dataframe and save to file
df = pd.DataFrame(np.concatenate((beta_joint_values, alpha_joint_values), axis=0).T, columns=['beta1', 'beta2', 'beta3', 'alpha1', 'alpha2', 'alpha3'])
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
df.to_csv('./video_data/joint_values_video_v2.csv', index=False)


