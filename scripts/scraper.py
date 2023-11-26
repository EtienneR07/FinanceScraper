import requests
from bs4 import BeautifulSoup
import time
from random import randint

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


def try_get(list, name, index, index2):
    if index >= len(list):
        return ''
    else:
        try:
            spans = list[index].find_all(name)
            if index2 >= len(spans):
                return ''
            else:
                return spans[index2].text
        except Exception as e:
            return ''


def extractOverview(symbol):
    url = f"https://www.marketwatch.com/investing/stock/{symbol}"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find("ul", "list list--kv list--col50").find_all('li')
    open = try_get(list, 'span', 0, 0)
    shares_outstanding = try_get(list, 'span', 4, 0)
    eps = try_get(list, 'span', 9, 0)
    return {
        "symbol": symbol,
        "openingPrice": open,
        "sharesOutstanding": shares_outstanding,
        "eps": eps
    }


def extractProfile(symbol):
    url = f"https://www.marketwatch.com/investing/stock/{
        symbol}/company-profile?mod=mw_quote_tab"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    tables = soup.find_all('table', 'table value-pairs no-heading')
    pe = try_get(tables, 'td', 0, 1)
    price_to_book = try_get(tables, 'td', 0, 9)
    debt_to_equity = try_get(tables, 'td', 4, 1)
    current_ratio = try_get(tables, 'td', 2, 1)
    return {
        "pe": pe,
        "priceToBook": price_to_book,
        "debtToEquity": debt_to_equity,
        "currentRatio": current_ratio
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
        sleepTime1 = randint(6, 10)
        sleepTime2 = randint(3, 5)
        time.sleep(sleepTime1)
        result_from_overview = extractOverview(lines[i].strip())
        time.sleep(sleepTime2)
        result_from_profile = extractProfile(lines[i].strip())
        combined_data = {**result_from_overview, **result_from_profile}
        with open(file_path, 'a') as file:
            file.write(f"{combined_data},\n")
        with open(index_file_path, 'w') as file:
            file.write(str(last_processed_index))
        last_processed_index = last_processed_index + 1
    except Exception as e:
        print(f"{e}")

print('All done')
