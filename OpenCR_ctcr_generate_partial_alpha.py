import numpy as np
import pandas as pd

np.random.seed(520)
N_sample = 100000
L1 = 15
L2 = 21.5
L3 = 27.5
MB = np.array([[-L1, 0, 0],
               [-L1, L1-L2, 0],
               [-L1, L1-L2, L2-L3],])

# Generate random joint values
beta_joint_values_01 = np.random.rand(3, N_sample)
beta_joint_values = MB @ beta_joint_values_01
alpha_joint_values = (np.random.rand(3, N_sample) - 0.5) * 2 * np.pi/3 * 4

s = - (beta_joint_values**2).sum(0) + ((alpha_joint_values-8*np.pi)**2).sum(0) * 2
s_ids = s.argsort()
print(s_ids.shape)
beta_joint_values = beta_joint_values[:,s_ids]
alpha_joint_values = alpha_joint_values[:,s_ids]

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
df.to_csv('joint_values_partial_new_oct17.csv', index=False)

