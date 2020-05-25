import numpy as np
import pandas as pd
import requests
from datetime import date
from dataBase.dataQuarry import *

class Stocks:
    def __init__(self):

# Creating DataFrame with all usa stocks and filter in to stocks in range of 0.2 < stocks < 10
        self.all_us_stocks = requests.get('https://financialmodelingprep.com/api/v3/company/stock/list?apikey=2c50c486fd2834b02f93e296db5d3742')
        self.all_us_stocks = self.all_us_stocks.json()
        self.a = pd.DataFrame(self.all_us_stocks)

        self.all_us_stocks_df = pd.DataFrame.from_dict(self.all_us_stocks['symbolsList'])

# From now in all_us_stocks_df will hold stpcks in the range 10 > all_us_stocks_df > 0.2
        self.all_us_stocks_df = self.all_us_stocks_df[self.all_us_stocks_df.price > 0.2]
        self.all_us_stocks_df = self.all_us_stocks_df[self.all_us_stocks_df.price < 10]
        self.all_us_stocks_df = self.all_us_stocks_df.sort_values(by='price', ascending=True)

# Create list out of symbol column
        self.stock_lst = self.all_us_stocks_df['symbol'].tolist()
        self.stock_lst_str = "'"+','.join(self.stock_lst)+"'"


    def cheap_stock_df(self):
        print(len(self.stock_lst))
        nn = self.stock_lst
        h = len(nn)/500
        print(h)
        print(int(h))
        m = len(self.stock_lst) / 7
        print(m)
        mm = len(self.stock_lst) - int(h)*500
        print(mm)


aa = Stocks()
aa.cheap_stock_df()