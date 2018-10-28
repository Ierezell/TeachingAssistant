"""This script is to extract values form stock market: see help"""
import argparse
import datetime
# mise en place des arguments
ARG = argparse.ArgumentParser(
    description='Extraction de valeurs historiques pour un symbole boursier')
ARG.add_argument(
    '-d', '--début', metavar='DATE', type=str,
    help='Date recherchée la plus ancienne (format: AAAA-MM-JJ)'
)
ARG.add_argument(
    '-f', '--fin', metavar='DATE',
    type=str, default=str(datetime.datetime.now().date()),
    help='Date recherchée la plus récente (format: AAAA-MM-JJ)'
)
ARG.add_argument(
    '-v', '--valeur', type=str, default='fermeture',
    choices=['fermeture', 'ouverture', 'min', 'max', 'volume'],
    help='La valeur désirée (par défaut: fermeture)'
)
ARG.add_argument(
    "symbole", nargs='+', type=str, help='Nom du symbole boursier désiré'
)

# transformation des infos du argparse en un dictionnaire nommé Optimum
# transformation des infos du argparse en un dictionnaire args
ARGS = ARG.parse_args()

# condition par défault si la date de début n'est pas spécifiée
if ARGS.début is None:
    ARGS.début = ARGS.fin

# Conversion de la valeur en fonction des
# éléments de la liste provenant de Alpha Vantage
CONVERSION = {
    'ouverture': '1. open', 'max': '2. high',
    'min': '3. low', 'fermeture': '4. close', 'volume': '5. volume'
}
VALEUR_CHOISIE = ARGS.valeur
ARGS.valeur = CONVERSION[ARGS.valeur]

# Création d'une liste des jours entre début et fin
LISTE_DES_JOURS = []
START = datetime.datetime.strptime(ARGS.début, '%Y-%m-%d')
END = datetime.datetime.strptime(ARGS.fin, '%Y-%m-%d')
STEP = datetime.timedelta(days=1)
while START <= END:
    LISTE_DES_JOURS.append(START.date())
    START = START + STEP

# Identification de la date il y a cent jours
# 128 car il y avait 28 jours de weekends...
DATECENT = datetime.datetime.now() - datetime.timedelta(days=128)


def extraction(ordresymbolique):
    """Extraction de l'intervalle de jours voulue pour un symbole """
    url = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY'
    apikey = '3PQRLNKE9VP5JH12'

    import requests
    # Outputsize varie si la date de début est ou non cent jours avant.
    if DATECENT < datetime.datetime.strptime(ARGS.début, '%Y-%m-%d')\
            is True:
        thetype = 'compact'
    else:
        thetype = 'full'
    # Symbol variant en fonction de la liste des symboles fournies
    symbol = ARGS.symbole[ordresymbolique]

    params = {
        'function': function,
        'symbol': symbol,
        'apikey': apikey,
        'outputsize': thetype,
        }

    response = requests.get(url=url, params=params)

    import json

    response = json.loads(response.text)

    # Création de la liste du symbole avec toutes les valeurs requises
    # Création de la liste pour un symbole avec les valeurs requises
    liste = []
    for k, _ in enumerate(LISTE_DES_JOURS):
        try:
            liste.append(
                (str(LISTE_DES_JOURS[k]), response['Time Series (Daily)']
                 [str(LISTE_DES_JOURS[k])][ARGS.valeur])
            )
        except KeyError:
            pass
    return liste


# retour des informations sous le format demandé
BEGIN = datetime.datetime.strptime(ARGS.début, '%Y-%m-%d').date()
ENDING = datetime.datetime.strptime(ARGS.fin, '%Y-%m-%d').date()
for a in range(len(ARGS.symbole)):
    print(
        '{0}({1}, {2}, {3})'.format(
            ARGS.symbole[a], VALEUR_CHOISIE,
            BEGIN, ENDING
        )
    )
    print(extraction(a))
