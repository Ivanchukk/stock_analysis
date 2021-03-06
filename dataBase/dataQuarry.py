import sqlite3



class StockDataBase:
    def __init__(self, stocks):
        self.conn = sqlite3.connect(stocks)
        self.cur = self.conn.cursor()

    def add_data(self,company_quotes_df):
        company_quotes_df.to_sql(name='stocks',if_exists='append', con=self.conn)
        self.cur.execute("SELECT * FROM stocks")
        g = self.cur.fetchall()
        print(g)
        return g

    def retrieve_date(self, a):
        self.cur.execute("SELECT date, symbol, price,priceAvg50,priceAvg200, changesPercentage, change, volume, avgVolume, pe, eps FROM stocks")
        g = self.cur.fetchall()
        print(g)
        return g

        a = tuple(a)
        self.cur.execute("SELECT date, symbol, price,priceAvg50,priceAvg200, changesPercentage, change, volume, avgVolume, pe, eps  FROM stocks WHERE date in {}".format(a))
        g = self.cur.fetchall()
        return g

