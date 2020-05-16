import requests
import pandas as pd

histprices = requests.get("https://fmpcloud.io/api/v3/historical-price-full/GOOG?serietype=line&apikey=GOOG")
histprices = histprices.json()

print(histprices)