"""Extraction de valeurs historiques pour un symbole boursier"""
import argparse
from datetime import date, datetime
parser = argparse.ArgumentParser(
    description='Extraction de valeurs historiques pour un symbole boursier'
)
parser.add_argument(
    '-f', '--fin',
    metavar='DATE', dest='fin', default=str(date.today()),
    help='Date recherchée la plus récente (format: AAAA-MM-JJ)'
)


parser.add_argument(
    '-d', '--début',
    metavar='DATE', dest='début', default='fin',
    help='Date recherchée la plus ancienne (format: AAAA-MM-JJ)'
)


parser.add_argument(
    '-v', '--valeur',
    dest='valeur', default='fermeture',
    choices=['fermeture', 'ouverture', 'min', 'max', 'volume'],
    help='La valeur désirée (par défault: fermeture)'
)

parser.add_argument(
    'symbole', nargs='+', help='Nom du symbole boursier désiré'
)

args = parser.parse_args()  # Les éléments de la consoles sont tous récupérés.


def alpha(symbole):
    """Fonction pour récupérer les données sur Alphavatage"""
    import requests
    from json import loads

    url = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY'
    apikey = '25A8MZR248DOVS2H'

    symbol = symbole

    params = {
        'function': function,
        'symbol': symbol,
        'apikey': apikey,
        'outputsize': 'full',
        }

    response = requests.get(url=url, params=params)
    response = loads(response.text)
    return response


def jours(debut, fin):
    """Ma fonction pour avoir un itérable des jours entre deux dates."""
    from datetime import timedelta
    fin = datetime.strptime(fin, '%Y-%m-%d').date()
    if debut == 'fin':  # Un petit problème m'a forcé à trouver cette solution.
        args.début = args.fin
        yield fin
    else:
        debut = datetime.strptime(debut, '%Y-%m-%d').date()
        if debut > fin:
            raise IndexError('La date de début est après la date de fin.')
        else:
            delta = fin - debut
            for jour in range(delta.days + 1):
                yield debut + timedelta(jour)


dico = {'ouverture': '1', 'max': '2', 'min': '3', 'fermeture': '4',
        'volume': '5'}
dico2 = {'ouverture': 'open', 'max': 'high', 'min': 'low',
         'fermeture': 'close', 'volume': 'volume'}

for compagnie in args.symbole:  # Mes dernières étapes.
    valeurs = []
    responses = alpha(compagnie)
    for date in jours(args.début, args.fin):
        try:
            valeurs.append((str(date), responses['Time Series (Daily)']
                            [str(date)]
                            ['{}. {}'.format(dico[args.valeur],
                                             dico2[args.valeur])]))
        except KeyError:
            continue
    ma_chaine = '{}({}, {}, {})\n'.format(compagnie, args.valeur,
                                          datetime.strptime(args.début,
                                                            '%Y-%m-%d').date(),
                                          datetime.strptime(args.fin,
                                                            '%Y-%m-%d').date())
    if not valeurs:
        print('Valeur(s) non disponibles, vérifiez les dates ou le symbole.')
    else:
        print(ma_chaine, valeurs)
