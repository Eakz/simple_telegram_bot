import requests
import json


def quoting():
    if not read_json():
        quote, author = gquote()
        data = dict_f(quote, author)
        write_json(data)
        message = data['quotes'][-1]
        return message
    else:
        data = read_json()
        return data['quotes'][-1]


def gquote():
    quote_get = requests.get('http://quotes.rest/qod.json')
    quote = quote_get.json()['contents']['quotes'][0]['quote']
    author = quote_get.json()['contents']['quotes'][0]['author']
    author = '_'.join(author.split())
    return quote, author


def dict_f(quote, author, data=None):
    if not data:
        data = {}
        data['quotes'] = ['']
    quote_formatted = f'{quote}  |  @{author}'
    if data['quotes'][-1] != quote_formatted:
        data['quotes'].append(quote_formatted)
    return data


def read_json():
    try:
        with open('data.json') as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return


def write_json(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)
