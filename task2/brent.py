import requests
import json
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.nasdaq.com/',
    'Origin': 'https://www.nasdaq.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

params = {
    'assetclass': 'commodities',
    'fromdate': '2023-01-01',
    'limit': '9999',
    'todate': '2023-07-13',
}

def get_brent_dataframe():
    response = requests.get('https://api.nasdaq.com/api/quote/BZ%3ANMX/historical', params=params, headers=headers)
    json_dict = json.loads(response.text)
    data = json_dict["data"]["tradesTable"]["rows"]
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    df["volume"] = pd.to_numeric(df["volume"].str.replace(",", ""))
    df["close"] = pd.to_numeric(df["close"])
    df["open"] = pd.to_numeric(df["open"])
    df["high"] = pd.to_numeric(df["high"])
    df["low"] = pd.to_numeric(df["low"])
    df = df[["date", "close"]] # Data must be in unified format, and we only have date and close for TTF
    return df