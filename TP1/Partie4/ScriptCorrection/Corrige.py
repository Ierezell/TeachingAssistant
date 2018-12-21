import argparse
# import fire
import json
import requests
from datetime import date, timedelta

url = 'https://www.alphavantage.co/query'
function = 'TIME_SERIES_DAILY'
apikey = 'W1SUVOVMS71TME9S'

VALUES = {
    'ouverture': '1. open',
    'max': '2. high',
    'min': '3. low',
    'fermeture': '4. close',
    'volume': '5. volume',
}


def fetch_data_from_alphavantage(symbol, value='fermeture', start=None, end=None):
    days = (end-start).days+1
    params = {
        'function': function, 'symbol': symbol, 'apikey': apikey,
        'outputsize': 'full' if days > 100 else 'compact',
    }
    response = requests.get(url=url, params=params)
    response = json.loads(response.text)
    values = response['Time Series (Daily)']
    result = []
    for date in sorted(values.keys()):
        if start <= s2date(date) <= end:
            result.append((date, values[date][VALUES[value]]))
    return result


def s2date(value):
    '''Using the YYYY-MM-DD string format.'''
    year, month, day = map(int, value.split('-'))
    result = date(year=year, month=month, day=day)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Extraction de valeurs historiques pour un symbole boursier"
    )
    parser.add_argument(
        '-d', '--début', metavar='DATE', dest='start', default=None,
        type=s2date, help="Date recherchée la plus ancienne (format: AAAA-MM-JJ)"
    )
    parser.add_argument(
        '-f', '--fin', metavar='DATE', dest='end', default=date.today(),
        type=s2date, help="Date recherchée la plus récente (format: AAAA-MM-JJ)"
    )
    parser.add_argument(
        '-v', '--valeur', choices=['fermeture', 'ouverture', 'min', 'max', 'volume'],
        dest='value', default='fermeture', help="La valeur désirée (par défaut: fermeture)"
    )
    parser.add_argument(
        'symbols', nargs='+', metavar='symbole', help="Nom du symbole boursier désiré"
    )
    args = parser.parse_args()
    # result = fetch_historical_data(['aapl'])
    if args.start is None:
        args.start = args.end
    for symbol in args.symbols:
        print('{}({}, {}, {})'.format(symbol, args.value, args.start, args.end))
        print(fetch_data_from_alphavantage(
            symbol, args.value, args.start, args.end))
