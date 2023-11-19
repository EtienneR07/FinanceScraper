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
    url = f"https://www.marketwatch.com/investing/stock/aapl/company-profile?mod=mw_quote_tab"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    tables = soup.find_all('table', 'table value-pairs no-heading')
    valuationTableData = tables[0].find_all('td')
    liquidityTableData = tables[2].find_all('td')
    capitalizationTableData = tables[4].find_all('td')
    pe = valuationTableData[1].text
    priceToBook = valuationTableData[9].text
    debtToEquity = capitalizationTableData[1].text
    currentRatio = liquidityTableData[1].text
    return {
        "symbol": symbol,
        "pe": pe,
        "priceToBook": priceToBook,
        "debtToEquity": debtToEquity,
        "currentRatio": currentRatio
    }


stock_symbols_path = './scripts/stock_symbols.txt'
file_path = "./scripts/stocks_valuation_results.txt"
index_file_path = "./scripts/processing_index.txt"

try:
    with open(index_file_path, "r") as index_file:
        last_processed_index = int(index_file.read().strip())
except FileNotFoundError:
    last_processed_index = 0

with open(stock_symbols_path, "r") as stock_symbols:
    lines = stock_symbols.readlines()

for i in range(last_processed_index, len(lines)):
    try:
        sleepTime = randint(8, 32)
        time.sleep(sleepTime)
        result = extract(lines[i].strip())
        with open(file_path, 'a') as file:
            file.write(f"{result},\n")
        with open(index_file_path, 'w') as file:
            file.write(str(last_processed_index))
        last_processed_index = last_processed_index + 1
    except Exception as e:
        print(f"{e}")

print('All done')
