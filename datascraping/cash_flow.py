import requests
import numpy as np
import pandas as pd

desired_width=2000
pd.set_option('display.width', desired_width)

np.set_printoptions(linewidth=desired_width)

pd.set_option('display.max_columns', 30)

api_key = 'f5efebe214b2948db8e360ca7cde0307'

CF = requests.get(f'https://fmpcloud.io/api/v3/cash-flow-statement/AAPL?apikey={api_key}').json()

count= 0
#Create an empty dictionary
CF_3Y = {}
IS = requests.get(f'https://fmpcloud.io/api/v3/income-statement/AAPL?apikey={api_key}').json()

for item in CF:
  if count < 15:
    date = item['date']
    CF_3Y[date] = item
    #we add revenue as well to the dictionary since we need it to calculate the common-size cash flow
    CF_3Y[date]['Revenue'] = IS[count]['revenue']
    count += 1

CF_Common_Size = pd.DataFrame.from_dict(CF_3Y, orient='index')
CF_Common_Size = CF_Common_Size.T

Revenue = CF_Common_Size.iloc[-1]
CF_Common_Size = CF_Common_Size.iloc[4:-3,:]
CF_Common_Size = (CF_Common_Size/Revenue) * 100

#show as percentage:
pd.options.display.float_format = '{:.2f}%'.format
print(CF_Common_Size)