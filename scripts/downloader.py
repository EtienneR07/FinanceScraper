import requests
import csv
from bs4 import BeautifulSoup
import os

api_key = os.getenv("ALPHAVANTAGE_KEY")
apiUrl = f'https://www.alphavantage.co/query?function=LISTING_STATUS&date=2023-10-31&apikey={api_key}'

with requests.Session() as s:
    download = s.get(apiUrl)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    stock_symbols = [x[0] for x in list(cr)]

    file_path = "./scripts/stock_symbols.txt"
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as file:
        for symbol in stock_symbols:
            if '-' in symbol or symbol == 'symbol':
                continue
            file.write(f"{symbol.lower()}\n")
