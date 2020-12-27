import os, sys, io, base64
import pandas as pd, matplotlib.pyplot as plt , numpy as np
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import PSO as ParSwarm
import matplotlib.pyplot as plt

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Import data
#os.chdir('C:/Users/camerum/Desktop/Decision_Support_system/SsdWebApi/Models')
indices = ["FTSE_MIB", "All_Bonds", "SP_500"]
indicesName = ['C:/Users/camerum/Desktop/Decision_Support_system/SsdWebApi/Models/All_Bonds.csv', 'C:/Users/camerum/Desktop/Decision_Support_system/SsdWebApi/Models/FTSE_MIB.csv', 'C:/Users/camerum/Desktop/Decision_Support_system/SsdWebApi/Models/SP_500.csv']
datafrane=[]
result_forecasts = []
#df = pd.read_csv('All_Bonds.csv', usecols=['All_Bonds'], names=['SP_500'],header=0)
#df = pd.read_csv("C:/Users/camerum/Desktop/Decision_Support_system/SsdWebApi/Models/%s.csv" , delimiter=',', decimal='.', names=['values'], header=0, error_bad_lines=False)
#df = pd.read_csv("../%s.csv" % index, delimiter=',', decimal='.', names=['values'], header=0, error_bad_lines=False)
def print_figure(fig):
  """
  Converts a figure (as created e.g. with matplotlib or seaborn) to a png image and this 
  png subsequently to a base64-string, then prints the resulting string to the console.
  """
  buf = io.BytesIO()
  fig.savefig(buf, format='png')
  print(base64.b64encode(buf.getbuffer()))


#df2 = pd.read_csv('SP_500.csv',usecols=['SP_500'], header=0) # dataframe (series)
#plt.title('SP_500', color='black')
#df.plot()
#plt.show()
#to see all the component present in my serie 
#result = seasonal_decompose(df, model='multiplicative',freq=4)
#result.plot()

for i in indicesName:
      #datafrane = datafrane['values'].to_numpy()
      datafrane.append(pd.read_csv(i))
      #datafrane= datafrane.to_numpy()

print(datafrane[0].head())


 

plt.show()







# Accuracy metrics
def forecast_accuracy(forecast_val, test):

    rmse = np.mean((forcast - test)**2)**.523 # RMSE
    return({ 'rmse':rmse})


#Sarimax model  
from statsmodels.tsa.statespace.sarimax import SARIMAX
#for i in range(6):
    
def forcast(i):    
    aValues = datafrane[i].value() # array of values data
    print("test"+aValues)
    logdata = np.log(aValues) # log transform


    cutpoint = int(len(datafrane[i]) * 0.9)
    horizon_data_length = len(datafrane[i]) - cutpoint
    train = logdata[:cutpoint]
    test = logdata[cutpoint:]
  
    
    sarima_model = SARIMAX(train, order=(1,0,1), seasonal_order=(0,1,1,2), enforce_stationarity=False, enforce_invertibility=False)
    sfit = sarima_model.fit()
    print(sfit.summary())
    sfit.plot_diagnostics(figsize=(10, 6))
    plt.show()
    #print(sarima_model.summary())
    
    #dati di predicton non di forcast ancora detto prediction in sample
    
    ypred=sfit.predict(start=0,end=len(train))
    plt.plot(train)
    plt.plot(ypred)
    plt.title("trian")
    
    #previsione de dati quindi il forcat --->il modelo è stato esteso al futuro
    forewrap = sfit.get_forecast(steps=523)
    forecast_ci = forewrap.conf_int()
    forecast_val = forewrap.predicted_mean
    #forecast_val=forecast_val[1:]
    plt.plot(train)
    #plt.fill_between(forecast_ci.index,forecast_ci.iloc[:, 0],forecast_ci.iloc[:, 1], color='k', alpha=.25)
    plt.plot(forecast_val)
    plt.plot(test)
    plt.show()
    
    
    yfore = []
    for j in range(0, horizon_data_length):
        print("Actual {} {} {:.2f} forcast {:.2f}".format(i, j, test[j], forecast_val[j]))
        yfore.append(forecast_val[j])
        
    metrics = forecast_accuracy(forecast_val, test)
    print("RMSE is {}={:.2f} forecast{:.2f}".format(i ,metrics['rmse']))
    
    return yfore, horizon_data_length



#Predizioni in-sample: dei dati che conosco gia non interessante

'''
ypred = sfit.predict(start=0,end=len(train))
plt.plot(train)
plt.plot(ypred)
plt.show()
'''

if len(sys.argv) == 2:
    forcast(sys.argv[1])
else:
    print(len(indices))
    for i in range(len(indices)):
        print("e")
        f, horizon_data_length = forcast(indices[i])
        result_forecasts.append(f)
        
        
        
        
    portfolioInitialValue = 100000
    numvar = 7
    xmin = 0.05
    xmax = 0.7
    niter = 100
    popsize = 50
    nhood_size = 10
        
    PSO = ParSwarm.ParSwarmOpt(xmin, xmax)
    res = PSO.pso_solve(popsize, numvar, niter, nhood_size, portfolioInitialValue, horizon_data_length, result_forecasts)

    print("Portfolio: ", end='')
    for value in res.xsolbest:
        print(value, end=' ')
    print("")
    print("Return: {}".format(res.return_valuebest))
    print("Devst: {}".format(res.devstbest))