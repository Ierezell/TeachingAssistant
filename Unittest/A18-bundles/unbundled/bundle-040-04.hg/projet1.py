'''
Projet 1: Valeur boursière d'une action
'''
import argparse
import json
from datetime import date, datetime
import requests


def main():
    '''
    La fonction principale!!
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('symbole', nargs='+', metavar='symbole',
                        help='Nom du symbole boursier désiré')
    parser.add_argument('-d', '--début', metavar='DATE',
                        help='Date recherchée la plus ancienne (format: AAAA-MM-JJ)')
    parser.add_argument('-f', '--fin', metavar='DATE',
                        help='Date recherchée la plus récente (format: AAAA-MM-JJ)')
    parser.add_argument('-v', '--valeur', metavar='{fermeture,ouverture,min,max,volume}',
                        dest='mode',
                        default='fermeture',
                        choices={'fermeture', 'ouverture', 'min', 'max', 'volume'},
                        help='La valeur désirée (par défaut: fermeture)')

    args = parser.parse_args()

    symbol = args.symbole
    d_fin = str(date.today()) if args.fin is None \
        else datetime.strptime(args.fin, '%Y-%m-%d').strftime('%Y-%m-%d')
    d_debut = d_fin if args.début is None else datetime.strptime(args.début, '%Y-%m-%d').strftime(
        '%Y-%m-%d')
    mode = args.mode

    dic = {'ouverture': '1. open', 'max': '2. high', 'min': '3. low', 'fermeture': '4. close',
           'volume': '5. volume'}

    url = 'https://www.alphavantage.co/query'
    fonction = 'TIME_SERIES_DAILY'
    apikey = 'N1ZKW9R3YWZTF3KM'

    for sym in symbol:
        params = {
            'function': fonction,
            'symbol': sym,
            'apikey': apikey,
            'outputsize': 'compact',
        }

        response = requests.get(url=url, params=params)
        response = json.loads(response.text)

        liste = []
        liste.append((d_debut, response['Time Series (Daily)'][d_debut][dic[mode]]))
        liste.append((d_fin, response['Time Series (Daily)'][d_fin][dic[mode]]))

        print('{}({}, {}, {})'.format(sym, mode, d_debut, d_fin))
        print(liste)


if __name__ == '__main__':
    main()
