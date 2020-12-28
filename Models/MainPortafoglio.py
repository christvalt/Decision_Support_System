
#import pmdarima as pm # pip install pmdarima
from pandas.core.common import flatten
import os, sys, io, base64
import pandas as pd, matplotlib.pyplot as plt , numpy as np
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import PSO as ParSwarm
import matplotlib.pyplot as plt


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

indices = ["SP_500", "FTSE_MIB", "GOLD_SPOT", "MSCI_EURO", "All_Bonds", "SP_500", "SP_500"]

valoriDiforcast = []

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

    rmse = np.mean((forecast_val - test)**2)**.523 # RMSE
    return({ 'rmse':rmse})
from statsmodels.tsa.statespace.sarimax import SARIMAX

def forecast(id):
    
    df = pd.read_csv("../%s.csv" % id, sep=str, delimiter=',',names=['values'], header=0, error_bad_lines=False,warn_bad_lines=False,keep_default_na=True)
  #preprocessing 
  
    aValues = df['values'].to_numpy() # array of values data
    logdata = np.log(aValues) # log transform
    #logdiff=logdata.diff()
    cutpoint = int(len(df) * 0.91)
    horizon_data_length = len(df) - cutpoint
    train = logdata[:cutpoint]
    test = logdata[cutpoint:]
    
    ##Autocorrelazione more good
    import statsmodels.api as sm
    sm.graphics.tsa.plot_acf(df.values, lags=10)
    plt.show
   
  
    sarima_model = SARIMAX(train, order=(1,0,1), seasonal_order=(0,1,1,5), enforce_stationarity=False, enforce_invertibility=False)
    sfit = sarima_model.fit()
    print(sfit.summary())
    sfit.plot_diagnostics(figsize=(10, 6))
    #plt.show()
  
    # Predictions of y values based on "model", aka fitted values
   
    ypred=sfit.predict(start=0,end=len(train))
    forewrap = sfit.get_forecast(steps=horizon_data_length)
    #intervalo di forcast interessante
    forecast_ci = forewrap.conf_int()
    forecast_val = forewrap.predicted_mean
    #index_forecasts = pd.Series(range(df.index[-1] + 1 - horizon_data_length, df.index[-1] + 1))

    metrics = forecast_accuracy(forecast_val, test)
   # print("RMSE is {}={:.2f} forecast{:.2f}".format(i ,metrics['rmse']))

    yfore = []
    for j in range(0, horizon_data_length):
        #print("Actual {} {} {:.2f} forcast {:.2f}".format(i, j, test[j], forecast_val[j]))
        yfore.append(forecast_val[j])
  

    # Plot
    plt.clf()
    plt.plot(logdata)
    plt.plot(ypred, color='red', label='prediction onsample')
    plt.plot(yfore,linewidth=2, markersize=12)
    plt.plot([None for i in ypred] + [x for x in yfore])
    plt.title(" dati quindi  di forcat{}".format(id))
    #plt.legend()
    
  
    #plt.show()
    print_figure(plt.gcf())
    
    return yfore, horizon_data_length

if len(sys.argv) == 2:
   # forecast(sys.argv[1])
   print(sys.argv[1])
else:
    for i in range(len(indices)):
        f, horizon_data_length = forecast(indices[i])
        valoriDiforcast.append(f)
        
    portfolioInitialValue = 100000
    numvar = 7
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
   