import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import os, sys, io, base64
import PSO as ParSwarm

indices = ["FTSE_MIB", "All_Bonds", "esempio", "SP_500", "sta", "FTSE_MIB (2)", "esempio"]
result_forecasts = []


# 011 011

'''
prendi la mia seria la si lavora e genera una lunga stinga che contiene una imagine 

******nella cartella server dentro model devo fare python forcastStat.py seriea_storica.csv  
'''

def print_figure(fig):
	"""
	Converts a figure (as created e.g. with matplotlib or seaborn) to a png image and this 
	png subsequently to a base64-string, then prints the resulting string to the console.
	"""
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	print(base64.b64encode(buf.getbuffer()))


if __name__ == "__main__":
   # change working directory to script path
   abspath = os.path.abspath(__file__)
   dname = os.path.dirname(abspath)
   os.chdir(dname)

   print('MAPE Number of arguments:', len(sys.argv))
   print('MAPE Argument List:', str(sys.argv), ' first true arg:',sys.argv[1])   
   
  # dffile = sys.argv[1]
   #df.plot()  
   
   
'''
   #another corelation more good
   import statsmodels.api as sm
   sm.graphics.tsa.plot_acf(df, lags=500)
'''

def forcast(id):
       dffile = sys.argv[1]
       #df = pd.read_csv("C:/Users/camerum/Desktop/Decision_Support_system/SsdWebApi/Models/"+dffile % id , names=['values'],header=0)
       df = pd.read_csv("../%s.csv" % id, delimiter=',', decimal='.', names=['values'], header=0, error_bad_lines=False)

           #Preprocessing: log transform
       npa = df['values'].to_numpy()
       logdata = np.log(npa)
       logdata=pd.Series(logdata)
       difflog = logdata.diff()
       difflog=difflog[0:]
       #plt.plot(df)
       #slpit dei dati
       cutpoint = int(0.91*len(difflog))
       train = difflog[:cutpoint]
       test = difflog[cutpoint:]
       orizonte_temporale = len(difflog) - cutpoint
    
    #Sarimax model  
       from statsmodels.tsa.statespace.sarimax import SARIMAX
       sarima_model = SARIMAX(train, order=(1,0,1), seasonal_order=(0,1,1,2), enforce_stationarity=False, enforce_invertibility=False)
       sfit = sarima_model.fit()
       print(sfit.summary())
       #sfit.plot_diagnostics(figsize=(10, 6))
       #plt.show()
       #print(sarima_model.summary())
        
       #dati di predicton non di forcast ancora detto prediction in sample
        
       ypred=sfit.predict(start=0,end=len(train))
       #plt.plot(train)
       #plt.plot(ypred)
       #plt.title("trian")
        
       #previsione de dati quindi il forcat --->il modelo è stato esteso al futuro
       forewrap = sfit.get_forecast(steps=orizonte_temporale)
       forecast_ci = forewrap.conf_int()
       forecast_val = forewrap.predicted_mean
       #forecast_val=forecast_val[1:]
       #plt.plot(train)
       #plt.fill_between(forecast_ci.index,forecast_ci.iloc[:, 0],forecast_ci.iloc[:, 1], color='red', alpha=.25)
       #plt.plot(forecast_val)
       #plt.plot(test)
       #plt.show()
       
       ypred = pd.Series(ypred)
       expdata = np.exp(ypred) # unlog
       plt.plot(expdata)
       expfore = np.exp(forecast_val)
       #plt.plot(forecast_val)
       #plt.plot([None for x in range(12)]+[x for x in expdata[12:]])
       #plt.plot(df)
       #plt.plot(reconstruct)
       #plt.plot([None for x in expdata]+[x for x in expfore])
       
       valutation=forecast_accuracy(forecast_val, test)
       print("rmse is {}:" +valutation)
       yfore = []
       for j in range(0, orizonte_temporale):
        print("Actual {} {} {:.2f} forecast {:.2f}".format(id, j, test[j], forecast_val[j]))
        yfore.append(forecast_val[j])
        plt.plot(difflog)
        print_figure(plt.gcf())
        return yfore, orizonte_temporale

# Accuracy metrics
def forecast_accuracy(forcast, test):

    rmse = np.mean((forcast - test)**2)**.523 # RMSE
    return({ 'rmse':rmse})

   #sm.graphics.tsa.plot_acf(train.values, lags=100)
plt.show
#reconstruct = np.exp(np.r_[train,test].cumsum()+logdata[0])
#reconstruct = np.exp(np.r_[ypred,forecast_val].cumsum()+logdata[0])


#plt.show

#plt.show()
   
   # Finally, print the chart as base64 string to the console.
#print_figure(plt.gcf())



   