import numpy as np
import pandas as pd

N_sample = 300
L1 = 15
L2 = 21.5
L3 = 27.5
MB = np.array([[-L1, 0, 0],
               [-L1, L1-L2, 0],
               [-L1, L1-L2, L2-L3],])

# Generate random joint values
beta_joint_values_01 = np.ones((3, N_sample))
beta_joint_values = MB @ beta_joint_values_01
alpha_joint_values = np.zeros((3, N_sample))
alpha_joint_values[2,0:50] = np.linspace(0, 8*np.pi,50)
alpha_joint_values[2,50:100] = np.linspace(8*np.pi,0,50)
alpha_joint_values[1:3,100:150] = np.linspace(0, 8*np.pi,50)
alpha_joint_values[1:3,150:200] = np.linspace(8*np.pi,0,50)
alpha_joint_values[0:3,200:250] = np.linspace(0, 8*np.pi,50)
alpha_joint_values[0:3,250:300] = np.linspace(8*np.pi,0,50)


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
df.to_csv('joint_values_oct11_sysid.csv', index=False)
