import requests
import json
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://tradingeconomics.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://tradingeconomics.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

def get_urals_dataframe():
    response = requests.get(
        'https://markets.tradingeconomics.com/chart?s=urdb:com&interval=1w&span=5y&securify=new&url=/commodity/urals-oil&AUTH=x1vFeEihJPHP5zApL5g8%2BvasPT5XTFHCIFhnbLR6BAtPnZ%2BqbWyh%2FKKuokx%2BRjLv&ohlc=0',
        headers=headers,
    )
    json_dict = json.loads(response.text)
    data = json_dict["series"][0]["data"]
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%dT%X")
    df["close"] = df["y"]
    df = df[["date", "close"]]
    return df