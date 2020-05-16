import requests
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime
# Make run table bigger
desired_width=1200
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 15)


def valuecompany(quote):
 #getting the latest dividend
   dividend = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{quote}')
   dividend = dividend.json()
   dividend = dividend['financials']
   Dtoday = float(dividend[0]['Dividend per Share'])
   df = pd.DataFrame.from_dict(dividend)


   metrics = requests.get(f'https://financialmodelingprep.com/api/v3/company-key-metrics/{quote}')
   metrics = metrics.json()

   ROE = float(metrics['metrics'][0]['ROE'])
   payout_ratio = float(metrics['metrics'][0]['Payout Ratio'])

   sustgrwothrate = ROE * (1 - payout_ratio)
   #print(df[['date','Dividend per Share']])


   pd.core.common.is_list_like = pd.api.types.is_list_like



   start = datetime.datetime(2019, 2, 1)
   end = datetime.datetime(2020, 2, 27)

   Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
   RF = float(Treasury.iloc[-1])
   RF = RF / 100
   beta = requests.get(f'https://financialmodelingprep.com/api/v3/company/profile/{quote}')
   beta = beta.json()
   print(beta)
   beta = float(beta['profile']['beta'])



   start = datetime.datetime(2019, 2, 15)
   end = datetime.datetime(2020, 2, 15)
   SP500 = web.DataReader(['sp500'], 'fred', start, end)

   # Drop all Not a number values using drop method.
   SP500.dropna(inplace=True)

   SP500yearlyreturn = (SP500['sp500'].iloc[-1] / SP500['sp500'].iloc[0]) - 1
   df = pd.DataFrame(SP500)
   ke = RF + (beta * (SP500yearlyreturn - RF))
   DDM = (Dtoday * (1 + sustgrwothrate)) / (ke - sustgrwothrate)
   return DDM


print(valuecompany('JNJ'))
