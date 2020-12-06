import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import os, sys, io, base64
import pandas as pd, numpy as np
import os, matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf
import statsmodels.api as sm
import pmdarima as pm
from statsmodels.tsa.statespace.sarimax import SARIMAX

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
   
   dffile = sys.argv[1]
   df = pd.read_csv("C:/Users/camerum/Desktop/Decision_Support_system/SsdWebApi/Models/"+dffile)
   
   # preprocessing of data
#transform my data to and numpy array 
npa = df.to_numpy() # array of indice data
plt.show()
#firt differenciate (optional because we will make it in our ARIMA model(d=1)
diffdata = df.diff()
#diffdata[0] = df['SP_500'][0] # reset 1st elem

# splitting of data 90-10

cutpoint = int(0.9*len(df))
train = df[:cutpoint]
test = df[cutpoint:]


#another corelation more good
import statsmodels.api as sm
sm.graphics.tsa.plot_acf(train.values, lags=440)
plt.show



model = pm.auto_arima(train.values, start_p=1, start_q=1,
                        test='adf', max_p=3, max_q=3, m=5,
                        start_P=1, seasonal=True,
                        d=1, D=1, trace=True,
                        error_action='ignore',
                        suppress_warnings=True,
                        stepwise=True) # False full grid
print(model.summary())
morder = model.order; print("Sarimax order {0}".format(morder))
mseasorder = model.seasonal_order;
print("Sarimax seasonal order {0}".format(mseasorder))

fitted = model.fit(train.values)
yfore = fitted.predict(n_periods=480) # forecast
ypred = fitted.predict_in_sample()
plt.plot(train.values)
plt.plot(ypred)

   
plt.plot(df)
plt.plot(yfore)
   #plt.show()
   
   # Finally, print the chart as base64 string to the console.
print_figure(plt.gcf())
#print the forcast value
print('Actual:', yfore)  
   

   