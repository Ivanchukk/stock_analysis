import numpy as np
import pandas as pd
import requests
from datetime import date
from dataBase.dataQuarry import *
import plotly.express as px

# Connection to sqllite3 database
stock_db = StockDataBase('stocks')

# Make run table bigger
desired_width=1200
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 30)

# Creating DataFrame with all usa stocks and filter in to stocks in range of 0.2 < stocks < 10
all_us_stocks = requests.get('https://financialmodelingprep.com/api/v3/company/stock/list')
all_us_stocks = all_us_stocks.json()

all_us_stocks_df = pd.DataFrame.from_dict(all_us_stocks['symbolsList'])

# From now in all_us_stocks_df will hold stpcks in the range 10 > all_us_stocks_df > 0.2
all_us_stocks_df = all_us_stocks_df[all_us_stocks_df.price > 0.2]
all_us_stocks_df = all_us_stocks_df[all_us_stocks_df.price < 10]
all_us_stocks_df = all_us_stocks_df.sort_values(by='price', ascending=True)

# Create list out of symbol column
stock_lst = all_us_stocks_df['symbol'].tolist()
stock_lst_str = ','.join(stock_lst)

# Creating DataFrame with company daily closing quotes
stock = ['JFKKW,CBL,MLGML.PA,AXAS,KMPH,GXE.TO']

company_quotes = requests.get(f'https://financialmodelingprep.com/api/v3/quote/{stock}')
company_quotes = company_quotes.json()

# Converting to DataFrame
company_quotes_df = pd.DataFrame.from_dict(company_quotes)


# Create row with current date
today_date = date.today()
company_quotes_df['date'] = today_date
company_quotes_df = company_quotes_df[['date', 'symbol', 'price', 'changesPercentage', 'change', 'volume', 'avgVolume']]


def a(company_quotes_df):
    print(company_quotes_df)
    stock_db.add_data(company_quotes_df)

#a(company_quotes_df)
dates = ['2020-05-16', '2020-05-17', '2020-05-18']
def b(dates):
    b = stock_db.retrieve_date(dates)
    c = pd.DataFrame(b)
    print(c)

b(dates)


