import numpy as np
import pandas as pd
import requests
from datetime import date
from dataBase.dataQuarry import *
import plotly.express as px

# Connection to sqllite3 database
stock_db = StockDataBase('stocks')

# Make run table bigger
desired_width = 1200
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 30)


class Stocks:
    def __init__(self):

        # Creating DataFrame with all usa stocks and filter in to stocks in range of 0.2 < stocks < 10
        self.all_us_stocks = requests.get(
            'https://financialmodelingprep.com/api/v3/company/stock/list?apikey=2c50c486fd2834b02f93e296db5d3742')
        self.all_us_stocks = self.all_us_stocks.json()
        self.a = pd.DataFrame(self.all_us_stocks)

        self.all_us_stocks_df = pd.DataFrame.from_dict(self.all_us_stocks['symbolsList'])

        # From now in all_us_stocks_df will hold stpcks in the range 10 > all_us_stocks_df > 0.2
        self.all_us_stocks_df = self.all_us_stocks_df[self.all_us_stocks_df.price > 0.2]
        self.all_us_stocks_df = self.all_us_stocks_df[self.all_us_stocks_df.price < 10]
        self.all_us_stocks_df = self.all_us_stocks_df.sort_values(by='price', ascending=True)

        # Create list out of symbol column
        self.stock_lst = self.all_us_stocks_df['symbol'].tolist()
        self.stock_lst_str = "'" + ','.join(self.stock_lst) + "'"

    # Creating DataFrame with company daily closing quotes
    def cheap_stock_df(self):
        df = pd.DataFrame()
        number_of_symbols = 500
        n = 0
        nnn = 0
        nn = self.stock_lst
        divider = len(self.stock_lst) / number_of_symbols
        remainder = len(self.stock_lst) - int(divider) * number_of_symbols

        while n <= len(self.stock_lst):
            if n < int(divider) * number_of_symbols:
                addition = number_of_symbols
            else:
                addition = remainder

            stock_lst = self.all_us_stocks_df['symbol'].tolist()
            small_stock_lst = stock_lst[n:n + addition]
            stock_lst_str1 = "'" + ','.join(small_stock_lst) + "'"
            company_quotes = requests.get(
                f'https://financialmodelingprep.com/api/v3/quote/{stock_lst_str1}?apikey=2c50c486fd2834b02f93e296db5d3742')
            company_quotes = company_quotes.json()
            company_quotes_df = pd.DataFrame.from_dict(company_quotes)

            df = df.append(company_quotes_df)
            nnn += number_of_symbols
            if nnn < divider * number_of_symbols:
                n += number_of_symbols
            else:
                n += remainder

        print(df)
        today_date = date.today()
        df['date'] = today_date
        company_quotes_df = df[
            ['date', 'symbol', 'price', 'priceAvg50', 'priceAvg200', 'changesPercentage', 'change', 'volume',
             'avgVolume', 'pe', 'eps']]
        return company_quotes_df

    def add_new_data_to_sql(self):
        a = self.cheap_stock_df()
        stock_db.add_data(a)


# aa = Stocks()
# aa.add_new_data_to_sql()


dates = ['2020-05-16', '2020-05-20', '2020-05-19']


def get_data_from_sql(dates):
    b = stock_db.retrieve_date(dates)
    c = pd.DataFrame(b, columns=['date', 'symbol', 'price', 'priceAvg50', 'priceAvg200', 'changesPercentage', 'change',
                                 'volume', 'avgVolume', 'pe', 'eps'])
    # c = c.iloc[:,1:]
    # uniq = c['date'].unique()
    # print(uniq)
    print(c)


# add_new_data_to_sql(aa.cheap_stock_df().company_quotes_df)
get_data_from_sql(dates)
