# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 15:17:25 2020

@author: Hp
"""

import pandas as pd, numpy as np
import os, matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf
import statsmodels.api as sm
import pmdarima as pm
from statsmodels.tsa.statespace.sarimax import SARIMAX



# change working directory to script path

os.chdir('C:/Users/camerum/Desktop/Decision_Support_system/SsdWebApi/Models')

df = pd.read_csv('SP_500.csv',usecols=['SP_500'], header=0) # dataframe (series)
plt.title('SP_500', color='black')

# preprocessing of data
#transform my data to and numpy array 
npa = df['SP_500'].to_numpy() # array of indice data
plt.show()
#firt differenciate (optional because we will make it in our ARIMA model(d=1)
diffdata = df['SP_500'].diff()
diffdata[0] = df['SP_500'][0] # reset 1st elem

# splitting of data 90-10

cutpoint = int(0.9*len(df))
train = df[:cutpoint]
test = df[cutpoint:]


#another corelation more good
import statsmodels.api as sm
sm.graphics.tsa.plot_acf(train.values, lags=40)
plt.show


#one again acf
acfdata = acf(train,unbiased=True,nlags=340)
plt.bar(np.arange(len(acfdata)),acfdata)
plt.show



# auto arima

cfdata = acf(train,unbiased=True,nlags=280)
plt.bar(np.arange(len(cfdata)),cfdata)
plt.show

model = pm.auto_arima(train.values, start_p=1, start_q=1,
                        test='adf', max_p=3, max_q=3, m=5,
                        start_P=0, seasonal=True,
                        d=None, D=1, trace=True,
                        error_action='ignore',
                        suppress_warnings=True,
                        stepwise=True) # False full grid
print(model.summary())
morder = model.order; print("Sarimax order {0}".format(morder))
mseasorder = model.seasonal_order;
print("Sarimax seasonal order {0}".format(mseasorder))
fitted = model.fit(train)
yfore = fitted.predict(n_periods=280) # forecast
ypred = fitted.predict_in_sample()
plt.plot(train)
plt.plot(ypred)
plt.plot([None for i in ypred] + [x for x in yfore])
plt.xlabel('time');plt.ylabel('sales')
plt.show()