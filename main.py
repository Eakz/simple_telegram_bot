# """COVID-19 T_bot https://itproger.com/news/269?source=yt
#     and https://www.youtube.com/watch?v=a0VVDMGwS0k&list=WL&index=6&t=0s"""

# import COVID19Py
# covid19 = COVID19Py.COVID19()
# latest = covid19.getLatest()
# print(latest)

import requests

quote_get = requests.get('http://quotes.rest/qod.json')

quote = quote_get.json()['contents']['quotes'][0]['quote']
author = quote_get.json()['contents']['quotes'][0]['author']
permalink = quote_get.json()['contents']['quotes'][0]['permalink']
