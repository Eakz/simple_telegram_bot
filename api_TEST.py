import requests

response = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5');

print(response.json())