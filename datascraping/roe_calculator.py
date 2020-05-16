import numpy as np
import pandas as pd
import requests
import plotly.express as px

# Make run table bigger
desired_width=1200
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 15)

z = []


def get_roe(stock):
    # Getting Income Statement and Balance Sheet Data
    income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/financials/income-statement/{stock}?period=quarter")
    income_statement = income_statement.json()
    BS = requests.get(f"https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{stock}?period=quarter")
    BS = BS.json()
    print(BS)
    # Transfer Data into DataFrame
    df_BS = pd.DataFrame.from_dict(BS["financials"])
    df_income_statement = pd.DataFrame.from_dict(income_statement["financials"])

    # Create DataFrame with relevant data
    df_BS_TSE = df_BS[['date','Total shareholders equity']]
    df_income_statement_NIC = df_income_statement[['date', 'Net Income Com']]
    dfmerge = pd.merge(df_BS_TSE,df_income_statement_NIC, on='date')

    # Filtering DataFrame so that we get Annual data
    dfmerge['check'] = dfmerge['date'].str.contains('-03-')
    dfmerge = dfmerge[dfmerge.check == True]

    # Calculation ROE (in %) for DataFrame  - Will give DataFrame with ROE for one company, each row in a year
    dfmerge['Total shareholders equity'] = dfmerge['Total shareholders equity'].astype(float).div(1000000)
    dfmerge['Net Income Com'] = dfmerge['Net Income Com'].astype(float).div(1000000)
    dfmerge['DeltaTSE'] = (dfmerge['Total shareholders equity']+dfmerge['Total shareholders equity'].shift(-1))/2
    dfmerge['ROE'] = (dfmerge['Net Income Com'].div(dfmerge['DeltaTSE'])).mul(100)

    # Will take ROE of latest quarter
    net_inc_common1 = float(income_statement['financials'][0]['Net Income Com'])
    tot_equity_now = float(BS['financials'][0]['Total shareholders equity'])
    tot_equity_previous = float(BS['financials'][4]['Total shareholders equity'])
    Average_equity = (tot_equity_now + tot_equity_previous)/2
    ROE = net_inc_common1/Average_equity*100

    # Show LineGrath for one company ROE -- IF you run lots of stocks leave as a comment because this script open's
    # new window for each fig
    #fig = px.line(dfmerge, x="date", y="ROE", title=f'Net Debt {stock}')
    #fig.show()

    # Append stock to ROE for comparing all companies ROE
    z.append((stock,ROE))


# Will make DataFrame with X number of stock

def a():

    # Create DataFrame with all S&P stocks
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    dframe_list = pd.io.html.read_html(url)
    dframe = dframe_list[0]

    # Create List of Symblos out of S&P DataFrame
    list_sp500_symbols = dframe['Symbol'].to_list()
    list_sp500_symbols1 = list_sp500_symbols[:1]  # You need to insert number of stocks you want to run

    #  Will send X number of stocks to ROE function calculator
    for symbol in list_sp500_symbols1:
        get_roe(symbol)

    # Create two list to insert into dictionary

    symbol = []
    ROE = []
    for i, ii in z:
        symbol.append(i)
        ROE.append(ii)
    # Create DataFrame with new ROE column
    case = {'Symbol': symbol, 'ROE': ROE}
    casedataframe = pd.DataFrame.from_dict(case)
    mergeROE_dframe = pd.merge(dframe, casedataframe, on='Symbol')

    print(mergeROE_dframe)
a()



#Apple = getROE('AAPL')
##Format number as percentage
#Apple = "{:.2%}".format(Apple)
#
##MSFT = getROE('MSFT')
##MSFT = "{:.2%}".format(MSFT)
#
##print('MSFT:', MSFT )
#print('AAPL:', Apple )

