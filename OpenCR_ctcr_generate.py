import numpy as np
import pandas as pd

np.random.seed(520)
N_sample = 10000
L1 = 16
L2 = 22
L3 = 28.4
MB = np.array([[-L1, 0, 0],
               [-L1, L1-L2, 0],
               [-L1, L1-L2, L2-L3],])

# Generate random joint values
beta_joint_values_01 = np.random.rand(3, N_sample)
beta_joint_values = MB @ beta_joint_values_01
alpha_joint_values = np.random.rand(3, N_sample) * 2 * np.pi * 4 

# create a dataframe and save to file
df = pd.DataFrame(np.concatenate((beta_joint_values, alpha_joint_values), axis=0).T, columns=['beta1', 'beta2', 'beta3', 'alpha1', 'alpha2', 'alpha3'])
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
df.to_csv('beta_alpha_joint_values.csv', index=False)

