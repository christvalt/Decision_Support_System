
#import pmdarima as pm # pip install pmdarima
#from pandas.core.common import flatten
import os, sys, io, base64
import pandas as pd, matplotlib.pyplot as plt , numpy as np
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import PSO as ParSwarm
import matplotlib.pyplot as plt


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

serie = ["SP_500", "FTSE_MIB", "GOLD_SPOT", "MSCI_EM", "MSCI_EURO"]

valoriDiforcast = []
expdata=[]

def print_figure(fig):
	"""
	Converts a figure (as created e.g. with matplotlib or seaborn) to a png image and this 
	png subsequently to a base64-string, then prints the resulting string to the console.
	"""
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	print(base64.b64encode(buf.getbuffer()))

# Accuracy metrics
def forecast_accuracy(forecast_val, test):

    rmse = np.mean((forecast_val - test) ** 2) ** .0  # RMSE
    return({ 'rmse':rmse})
from statsmodels.tsa.statespace.sarimax import SARIMAX

def forecast(id):
    
    df = pd.read_csv("../%s.csv" % id, sep=str, delimiter=',',names=['values'], header=0, error_bad_lines=False,warn_bad_lines=False,keep_default_na=True)
  #preprocessing 
  
    dataframe = df['values'].to_numpy() # array of values data
    logdata = np.log(dataframe) # log transform
    #logdiff=logdata.diff()
    cutpoint = int(len(df) * 0.91)
    horizon_data_length = len(df) - cutpoint
    train = logdata[:cutpoint]
    train1 = dataframe[:cutpoint]
    test = logdata[cutpoint:]
    test=test[0:]
    
    ##Autocorrelazione more good
    import statsmodels.api as sm
    sm.graphics.tsa.plot_acf(df.values, lags=10)
    plt.show
   
  
    sarima_model = SARIMAX(train1, order=(1,0,1), seasonal_order=(0,1,1,5), enforce_stationarity=False, enforce_invertibility=False)
    sfit = sarima_model.fit()
    print(sfit.summary())
    sfit.plot_diagnostics(figsize=(10, 6))
    #plt.show()
   # index_forecasts = pd.Series(range(df.index[-1] - horizon_data_length, df.index[-1]))
   
    # Predictions of y values based on "model", aka fitted values
   #index_forecasts = pd.Series(range(df.index[-1]+1  - horizon_data_length, df.index[-1]+1))
    ypred=sfit.predict(start=0,end=len(train))
    forewrap= sfit.get_forecast(steps=horizon_data_length)
    #intervalo di forcast interessante
    forecast_ci = forewrap.conf_int()
    forecast_val = forewrap.predicted_mean
    forecast_val=forecast_val[0:]
    #forecast_ci=pd.Series(forecast_val, index=index_forecasts)
    re=pd.Series(range)
    
    metrics = forecast_accuracy(forecast_val, test)
    print("RMSE is "+id,metrics['rmse'])

    yfore = []
    for j in range(0, horizon_data_length):
        print("Actual {} forcast {:.2f}".format(id,forecast_val[j-1]))
        yfore.append(forecast_val[j-1])
       
    
  
    # Plot
    plt.clf()
    plt.plot(train1)
    plt.plot(ypred)
    plt.plot([None for i in ypred] + [x for x in yfore])
    plt.xlabel('time');plt.ylabel('sales')

    
    plt.title("ARIMA forecast of {}".format(id))
    plt.legend()
    
  
    #plt.show()
    print_figure(plt.gcf())
    # simple recosntruction
   # yfore1=yfore.pd()
    
    return yfore, horizon_data_length

if len(sys.argv) == 2:
    forecast(sys.argv[1])
  # print(sys.argv[1])
else:
    for i in range(len(serie)):
        f, horizon_data_length = forecast(serie[i])
        valoriDiforcast.append(f)
        
    portfolioInitialValue = 100000
    numvar = 5
    xmin = 0.05
    xmax = 0.7
    niter = 2
    popsize = 70
    nhood_size = 7
        #run optimizzation algorithm
    PSO = ParSwarm.ParSwarmOpt(xmin, xmax)
    res = PSO.pso_solve(popsize, numvar, niter, nhood_size, portfolioInitialValue, horizon_data_length, valoriDiforcast)
    print("test value is".format(numvar,popsize))
    #print portafoglio value %
    print("Portfolio: ", end='')
    for value in res.xsolbest:
        print(value, end=' ')
    print("")
    print("Return: {}".format(res.return_valuebest))
    print("Devst: {}".format(res.devstbest))
   
    #print("dd",sys.argv[1])
   