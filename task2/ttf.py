import requests
import json
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.theice.com/products/27996665/Dutch-TTF-Natural-Gas-Futures/data?marketId=5586285&span=2',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
}

params = {
    'getHistoricalChartDataAsJson': '',
    'marketId': '5586285',
    'historicalSpan': '2',
}

def get_ttf_dataframe():
    response = requests.get('https://www.theice.com/marketdata/DelayedMarkets.shtml', params=params, headers=headers)
    json_dict = json.loads(response.text)
    data = json_dict["bars"]
    dicts = []
    for row in data:
        dicts.append({"date": row[0], "close": row[1]})
    df = pd.DataFrame(dicts)
    df["date"] = pd.to_datetime(df["date"], format="%a %b %d %X %Y")
    return df
