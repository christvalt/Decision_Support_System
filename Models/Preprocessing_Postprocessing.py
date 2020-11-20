import pandas as pd, numpy as np
import os, matplotlib.pyplot as plt


# change working directory to script path
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

df = pd.read_csv('FTSE_MIB.csv') # dataframe (series)
df.plot(x='FTSE_MIB',y='FTSE_MIB')
plt.title('FTSE_MIB', color='black')
plt._show()
