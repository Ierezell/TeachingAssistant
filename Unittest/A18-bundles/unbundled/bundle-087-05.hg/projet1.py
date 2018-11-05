""".

Ce script extrait les valeurs historiques demandées pour un
symbole boursier spécifié et les affiche à l'écran.

Quelques valeurs à spécifier dans CONFIG pour le
fonctionnement de l'application:
  - url: adresse URL à utiliser pour récupérer les données.
  - fonction: type de requête à faire au serveur.
  - apikey: clé d'accès au serveur.

Ce script requiert que le module `requests` soit
préalablement installé sur la plateforme.

"""

from datetime import datetime as dt
import argparse
import json
import requests

CONFIG = {
    'url': 'https://www.alphavantage.co/query',
    'fonction': 'TIME_SERIES_DAILY',
    'apikey': 'PCXY21CZHT1WVB5W'
}

PARSER = argparse.ArgumentParser(
    description='Extraction de valeurs historiques pour un symbole boursier')

PARSER.add_argument('symbole', help='Nom du symbole boursier d\xe9sir\xe9')

PARSER.add_argument(
    '-d',
    '--d\xe9but',
    metavar='DATE',
    dest='debut',
    type=str,
    help='Date recherch\xe9e la plus ancienne (format: AAAA-MM-JJ)')

PARSER.add_argument(
    '-f',
    '--fin',
    metavar='DATE',
    dest='fin',
    type=str,
    help='Date recherch\xe9e la plus r\xe9cente (format: AAAA-MM-JJ)')

PARSER.add_argument(
    '-v',
    '--valeur',
    dest='valeur',
    default='fermeture',
    choices=['fermeture', 'ouverture', 'min', 'max', 'volume'],
    help='La valeur d\xe9sir\xe9e (par d\xe9faut: fermeture)')

ARGS = PARSER.parse_args()


def request(symbole: str,
            adresse: str,
            fonction: str,
            apikey: str,
            size: str = 'compact') -> dict:
    """.

    Cette fonction envoie une requête GET à l'adresse
    spécifiée et retourne les données reçues.

    """
    params = {
        'function': fonction,
        'symbol': symbole,
        'apikey': apikey,
        'outputsize': size
    }
    try:
        response = requests.get(url=adresse, params=params)
        response = json.loads(response.text)
        assert isinstance(response, dict), 'Format incorrect!'
        assert 'Error Message' not in response, response['Error Message']
    except AssertionError as msg:
        print('Une erreur est survenue lors de la'
              'requ\xeate envoy\xe9e \xe0 {}: \n'.format(adresse) +
              '\xab {} \xbb'.format(msg))
        exit()
    return response


def period(debut: str, fin: str) -> tuple:
    """.

    Cette fonction retourne la période à traiter
    sous forme d'un tuple contenant:
    1- la date de début;
    2- la date de fin;
    3- l'étendu de la période en jours;
    4- l'éloignement de la période traitée (>100jours?)

    """
    try:
        debut = dt.strptime(debut, '%Y-%m-%d').date()
        fin = dt.strptime(fin, '%Y-%m-%d').date()
        delta = (fin - debut).days
        latence = (dt.now().date() - fin).days
        assert delta > 0, 'La date de d\xe9but doit pr\xe9c\xe9der celle de ' \
                          'fin: (d\xe9but: {}) (fin: {})'.format(debut, fin)
    except AssertionError as msg:
        print('Les dates choisies posent probl\xe8me:\n{}'.format(msg))
        exit()
    except ValueError:
        print('Le format de ces dates pose probl\xe8me:'
              '(d\xe9but: {}) (fin: {})\n'.format(debut, fin) +
              'Format requis: AAAA-MM-JJ (exemple: 2018-12-31)')
        exit()
    return debut, fin, delta, latence


def formatage(donnees: dict, valeur: str, per: tuple) -> list:
    """.

    Cette fonction retourne les données reçues filtrées
    et formatées selon la valeur et les dates spécifiées.

    """
    try:
        cle = {
            'fermeture': '4. close',
            'ouverture': '1. open',
            'min': '3. low',
            'max': '2. high',
            'volume': '5. volume'
        }
        assert 'Time Series (Daily)' in donnees, 'Format de données inattendu.'
        contenu = donnees['Time Series (Daily)'].items()
        liste = list(
            (key, value[cle[valeur]]) for (key, value) in contenu
            if per[0] <= dt.strptime(key, '%Y-%m-%d').date() <= per[1])
    except AssertionError as msg:
        print('Une erreur s\'est produite lors du formatage des donn\xe9es'
              're\xe7ues:\n \xab {} \xbb'.format(msg))
        exit()
    return sorted(liste)


def display(symbole: str, valeur: str, debut: str, fin: str,
            donnees: list) -> None:
    """.

    Cette fonction affiche le résultat de la requête.

    """
    print('{}({}, {}, {})'.format(symbole, valeur, debut, fin))
    print(donnees)


def init(symbole: str, valeur: str, debut: str, fin: str,
         config: dict) -> None:
    """.

    Cette fonction initialise le script.

    """
    per = period(debut, fin)
    try:
        size = 'compact' if per[3] < 100 else 'full'
        req = request(symbole, config['url'], config['fonction'],
                      config['apikey'], size)
        form = formatage(req, valeur, per)
        display(symbole, valeur, debut, fin, form)
    except AssertionError as msg:
        print('Une erreur est survenue lors de l\'initialisation:\n'
              '\xab {} \xbb'.format(msg))
        exit()


# C'est ici que l'application s'initialise...
init(ARGS.symbole, ARGS.valeur, ARGS.debut, ARGS.fin, CONFIG)
