import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator


import seaborn as sns
import pandas as pd
import numpy as np
import os
import ParseResultFile as prs

cur_path = os.path.dirname(__file__)
result_file = os.path.join(cur_path, '..', 'results', 'data', '2021.08.01 - 17.06.44.txt')
print(result_file)
print('#'*30)
x,y,z,dateTime,limits = prs.GetResultsFromFile(result_file)

min_val = min(z)
max_val = max(z)

offset = z[0]
z= [dz - offset for dz in z]

df = pd.DataFrame.from_dict(np.array([x,y,z]).T)
df.columns = ['X_value','Y_value','Z_value']
df['Z_value'] = pd.to_numeric(df['Z_value'])

data= df.pivot('Y_value','X_value','Z_value')

Y = list(dict.fromkeys(y))
ax = sns.heatmap(data,vmin=min_val,vmax=max_val,center=0,annot=True,yticklabels=Y, linewidth=0.3)
ax.invert_yaxis()
ax.set_title(f'{dateTime}\n{limits} offset:{offset}')
plt.show()

