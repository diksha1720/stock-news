import requests
import datetime as dt
import math
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_api_key = ''
news_api_key = ''

FROM_NUMBER = ""
TO_NUMBER = ""

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'interval': '60min',
    'apikey': stock_api_key
}
news_params = {
    'q': COMPANY_NAME,
    'from': dt.datetime.now().date(),
    'sortBy': 'popularity',
    'apiKey': news_api_key,
    'language': 'en',

}

response = requests.get(STOCK_ENDPOINT, params=stock_params).json()
data = response["Time Series (Daily)"]

last_two_days = list(data.items())[:2]
prev_day_cp = float(last_two_days[0][1]['4. close'])
day_before_cp = float(last_two_days[1][1]['4. close'])

price_diff = (prev_day_cp - day_before_cp)
if price_diff < 0:
    symbol = '🔻'
else:
    symbol = '🔺'

price_perc = abs(price_diff / prev_day_cp) * 100

news_list = []
response_news = requests.get(NEWS_ENDPOINT, params=news_params)
for i in range(3):
    news_list.append(response_news.json()['articles'][i])

if price_perc >= 1:
    for i in range(3):
        msg = f"\n\n{STOCK}: {symbol}{math.floor(price_perc)}%\n\nHeadline:\n{news_list[i]['title']}.\n\nBrief:\n{news_list[i]['description']}."
        message = client.messages \
            .create(
            body=msg,
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )
