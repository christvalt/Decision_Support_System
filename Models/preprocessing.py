import pandas as pd, numpy as np
import os, matplotlib.pyplot as plt
import pmdarima as pm # pip install pmdarima
import pandas as pd

# change working directory to script path
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir('C:/Users/camerum/Desktop/Decision_Support_system/SsdWebApi/Models')




df = pd.read_csv('/FTSE_MIB.csv', names=['FTSE_MIB'], header=0)
ds = df.sales
model = pm.auto_arima(ds.values, start_p=1, start_q=1,
test='adf', max_p=3, max_q=3, m=4,
start_P=0, seasonal=True,
d=None, D=1, trace=True,
error_action='ignore',
suppress_warnings=True,
stepwise=True) # False full grid
print(model.summary())
morder = model.order
mseasorder = model.seasonal_order
fitted = model.fit(ds)
yfore = fitted.predict(n_periods=4) # forecast
ypred = fitted.predict_in_sample()
plt.plot(ds.values)
plt.plot(ypred)
plt.plot([None for i in ypred] + [x for x in yfore])
plt.xlabel('time');plt.ylabel('sales')

plt.show()


