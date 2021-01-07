import os, sys, io, base64
import pmdarima as pm # pip install pmdarima
import numpy as np
import pandas as pd
from pandas.core.common import flatten
import PSO as ParSwarm
import matplotlib.pyplot as plt

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

indices = ["SP_500", "FTSE_MIB", "GOLD_SPOT", "MSCI_EM", "MSCI_EURO", "All_Bonds", "US_Treasury"]

result_forecasts = []

def print_figure(fig):
	"""
	Converts a figure (as created e.g. with matplotlib or seaborn) to a png image and this 
	png subsequently to a base64-string, then prints the resulting string to the console.
	"""
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	print(base64.b64encode(buf.getbuffer()))

# Accuracy metrics
def forecast_accuracy(forecast, actual):
    mape = np.mean(np.abs(forecast - actual) / np.abs(actual))  # MAPE
    me = np.mean(forecast - actual)  # ME
    mae = np.mean(np.abs(forecast - actual))  # MAE
    mpe = np.mean((forecast - actual) / actual)  # MPE
    rmse = np.mean((forecast - actual) ** 2) ** .5  # RMSE
    corr = np.corrcoef(forecast, actual)[0, 1]  # corr
    mins = np.amin(np.hstack([forecast[:, None],
                              actual[:, None]]), axis=1)
    maxs = np.amax(np.hstack([forecast[:, None],
                              actual[:, None]]), axis=1)
    minmax = 1 - np.mean(mins / maxs)  # minmax
    return ({'mape': mape, 'me': me, 'mae': mae,
             'mpe': mpe, 'rmse': rmse,
             'corr': corr, 'minmax': minmax})

def forecast(index):
    df = pd.read_csv("../%s.csv" % index, delimiter=',', decimal='.', names=['values'], header=0, error_bad_lines=False)
  
    aValues = df['values'].to_numpy() # array of values data
    logdata = np.log(aValues) # log transform

    cutpoint = int(len(df) * 0.9)
    horizon_data_length = len(df) - cutpoint
    train = logdata[:cutpoint]
    test = logdata[cutpoint:]
  
    model = pm.auto_arima(train, start_p=1, start_q=1,
    test='adf', max_p=3, max_q=3,
    d=1, trace=True,
    error_action='ignore',
    suppress_warnings=True,
    stepwise=True) # False full grid
  
    # Predictions of y values based on "model", aka fitted values
    ypred = model.predict_in_sample(start=1, end=len(train))
    forecasts, confint = model.predict(n_periods=horizon_data_length, return_conf_int=True)
    index_forecasts = pd.Series(range(df.index[-1] + 1 - horizon_data_length, df.index[-1] + 1))

    metrics = forecast_accuracy(forecasts, np.array(list(flatten(df.values[-horizon_data_length - 1:-1]))))
    print("MAPE {} = {:.2f}".format(index, metrics['mape']))

    yfore = []
    for j in range(0, horizon_data_length):
        print("Actual {} {} {:.2f} forecast {:.2f}".format(index, j, test[j], forecasts[j]))
        yfore.append(forecasts[j])
  
    # make series for plotting purpose
    fitted_series = pd.Series(forecasts, index=index_forecasts)
    lower_series = pd.Series(confint[:, 0], index=index_forecasts)
    upper_series = pd.Series(confint[:, 1], index=index_forecasts)

    # Plot
    plt.clf()
    plt.plot(logdata, label='LogData')
    plt.plot(ypred, color='brown', label='Predictions')
    plt.plot(fitted_series, color='darkgreen', label='Forecast')
    plt.fill_between(lower_series.index,
                     lower_series,
                     upper_series,
                     color='k', alpha=.15)
    plt.title("ARIMA forecast of {}".format(index))
    plt.legend()
  
    #plt.show()
    print_figure(plt.gcf())
    
    return yfore, horizon_data_length

if len(sys.argv) == 2:
    forecast(sys.argv[1])
else:
    for i in range(len(indices)):
        f, horizon_data_length = forecast(indices[i])
        result_forecasts.append(f)
        
    portfolioInitialValue = 100000
    numvar = 7
    xmin = 0.05
    xmax = 0.7
    niter = 2
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