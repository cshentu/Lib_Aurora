import numpy as np
import pandas as pd

N_sample = 10
L1 = 16
L2 = 22.25
L3 = 28.7
MB = np.array([[-L1, 0, 0],
               [-L1, L1-L2, 0],
               [-L1, L1-L2, L2-L3],])

# Generate random joint values
beta_joint_values_01 = np.random.rand(3, N_sample)
beta_joint_values = MB @ beta_joint_values_01
alpha_joint_values = np.random.rand(3, N_sample) * 2 * np.pi * 4 

# create a dataframe and save to file
df = pd.DataFrame(np.concatenate((beta_joint_values, alpha_joint_values), axis=0).T, columns=['beta1', 'beta2', 'beta3', 'alpha1', 'alpha2', 'alpha3'])
df.to_csv('beta_alpha_joint_values.csv', index=False)

