import os
import pandas as pd, matplotlib.pyplot as plt , numpy as np
from statsmodels.tsa.arima_model import ARIMA
# Import data
os.chdir('C:/Users/camerum/Desktop/Decision_Support_system/SsdWebApi/Models')
df = pd.read_csv('All_Bonds.csv', usecols=[0], names=['value'],header=0)





cutpoint = int(0.7*len(df))
train = df[:cutpoint]
test = df[cutpoint:]
 
#da mettere nella directory Model 
#vwerra chiamato dal server c#
#lege dei dati lo metti in un data frame poi fai qualche analisi(preprossesing ,prediction)

#plot initial data frame 
df.plot()
plt.title('initial train set', color='black')
plt.show()
 
#Preprocessing: log transform
npa = df.to_numpy()
logdata = np.log(npa)
plt.plot(npa, color = 'blue', marker = "o")
plt.plot(logdata, color = 'red', marker = "o")
plt.title("numpy.log()")
plt.xlabel("x");plt.ylabel("logdata")
#plt.show() 


#Autocorrelazione

from statsmodels.tsa.stattools import acf

diffdata = df.value.diff()
diffdata[0] = df.value[0] # reset 1st elem
acfdata = acf(diffdata,unbiased=True,nlags=50)
plt.bar(np.arange(len(acfdata)),acfdata)
plt.show


# oppure
import statsmodels.api as sm
diffdata = df.value.diff()
diffdata[0] = df.value[0] # reset 1st elem
sm.graphics.tsa.plot_acf(diffdata, lags=100)
plt.title("aoooooto")
plt.show


#division , train and test set
#cutpoint = int(0.7*len(diffdata))
#train = diffdata[:cutpoint]
#test = diffdata[cutpoint:]



# 1,1,2 ARIMA Model (p,d,q)
'''
model = ARIMA(train.value, order=(3,0,2))
model_fit = model.fit(disp=0)
print(model_fit.summary())

# Plot residual errors
residuals = pd.DataFrame(model_fit.resid)
fig, ax = plt.subplots(1,2)
residuals.plot(title="Residuals", ax=ax[0])
residuals.plot(kind='kde', title='Density', ax=ax[1])
plt.show()
'''

#Sarimax model  
from statsmodels.tsa.statespace.sarimax import SARIMAX
sarima_model = SARIMAX(train, order=(1,1,1), seasonal_order=(0,1,1,12))
sfit = sarima_model.fit()
sfit.plot_diagnostics(figsize=(10, 6))
plt.show()

#previsione de dati quindi il forcat --->il modelo è stato esteso al futuro
forewrap = sfit.get_forecast(steps=100)
forecast_ci = forewrap.conf_int()
forecast_val = forewrap.predicted_mean
plt.plot(train)
plt.fill_between(forecast_ci.index,forecast_ci.iloc[:, 0],forecast_ci.iloc[:, 1], color='k', alpha=.25)
plt.plot(forecast_val)
plt.show()


#Predizioni in-sample: dei dati che conosco gia non interessante

'''
ypred = sfit.predict(start=0,end=len(train))
plt.plot(train)
plt.plot(ypred)
plt.show()
'''






