import requests
from bs4 import BeautifulSoup
import time
from random import randint
import json
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


def extract(symbol):
    url = f"https://www.marketwatch.com/investing/stock/{symbol}/company-profile?mod=mw_quote_tab"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    tables = soup.find_all('table', 'table value-pairs no-heading')
    valuationTableData = tables[0].find_all('td')
    capitalizationTableData = tables[4].find_all('td')
    pe = valuationTableData[1].text
    priceToBook = valuationTableData[9].text
    debtToEquity = capitalizationTableData[1].text
    return {
        "symbol": symbol,
        "pe": pe,
        "priceToBook": priceToBook,
        "debtToEquity": debtToEquity
    }


stock_symbols = open('./scripts/stock_symbols.txt', 'r')
# lines = stock_symbols.readlines()
file_path = "./scripts/stocks_valuation_results.txt"
lines = ['goog', 'meta', 'amzn', 'tsla', 'nflx']
if os.path.exists(file_path):
    os.remove(file_path)
try:
    for line in lines:
        sleepTime = randint(5, 30)
        time.sleep(sleepTime)
        result = extract(line)
        with open(file_path, 'a') as file:
            file.write(f"{result},\n")
except Exception as e:
    print(f"{e}")

print('All done')
