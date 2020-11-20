import pandas as pd, numpy as np, os
import matplotlib.pyplot as plt
import pmdarima as pm # pip install pmdarima
from statsmodels.tsa.stattools import acf
# data upload
os.chdir('C:/Users/camerum/Desktop/Decision_Support_system/SsdWebApi/Models')
df = pd.read_csv('gioiellerie.csv', header=0)
df["period"] = df["year"].map(str) +"-" + df["month"].map(str)
df['period'] = pd.to_datetime(df['period'], format="%Y-%m").dt.to_period('M')
#df=df.set_index()
#df = df.set_index('period')
aSales = df['sales'].to_numpy() # array of sales data
logdata = np.log(aSales) # log transform
data = pd.Series(logdata) # convert to pandas series
plt.rcParams["figure.figsize"] = (10,8) # redefines figure size
plt.plot(data.values);plt.show
