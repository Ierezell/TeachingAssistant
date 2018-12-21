""".

Ce module contient deux fonctionnalités principales. La première est gérée par
la classe Date et sert à travailler avec différents formats de dates. La
seconde est gérée par la classe MarchéBoursier et sert à extraire des
informations boursières.

Quelques valeurs à spécifier dans CONFIG pour le
fonctionnement de l'application:
  - url: adresse URL à utiliser pour récupérer les données.
  - fonction: type de requête à faire au serveur.
  - apikey: clé d'accès au serveur.
  - cache: un nombre entier représentant la durée (en minutes) de validité du
    cache utilisé afin d'éviter d'envoyer inutilement plusieurs requêtes au
    serveur.

Ce script requiert que le module `requests` soit préalablement installé sur
la plateforme. De plus, il requiert que le module `outils` développé dans le
cadre du même projet.

Ce projet est conçu dans le cadre du cours GLO-1901.
Conçu par : Junior Cortentbach, Nguyễn Huy Dũng et René Chenard
Présenté à : Marc Parizeau

"""

import json
import requests
from outils import Date, ErreurDate

CONFIG = {
    'url': 'https://www.alphavantage.co/query',
    'fonction': 'TIME_SERIES_DAILY',
    'apikey': 'PCXY21CZHT1WVB5W',
    'cache': 1
}

class MarchéBoursier:
    """.

    Cette classe sert essentiellement à extraire de l'information concernant
    certains symboles boursiers, tel que la valeur d'un indice boursier à une
    date spécifiée.

    """

    configurations = {}
    __req_caches = {}

    def __init__(self, configurations: dict = None) -> None:
        """.

        La classe MarchéBoursier est initialisée avec les valeurs de
        configuration fournies. Autrement, les valeurs par défaut contenu dans
        CONFIG sont appliquées.

        """
        try:
            configurations = configurations if configurations else CONFIG
            assert isinstance(configurations, dict), 'Format incorrect!'
            assert 'url' in configurations, 'URL non d\xe9finie!'
            assert 'fonction' in configurations, 'Fonction non d\xe9finie!'
            assert 'apikey' in configurations, 'Cl\xe9 d\'API non d\xe9finie!'
            self.configurations['url'] = configurations['url']
            self.configurations['fonction'] = configurations['fonction']
            self.configurations['apikey'] = configurations['apikey']
            self.configurations['cache'] = configurations['cache'] if \
                configurations['cache'] else 1
        except AssertionError as msg:
            print('Une erreur est survenue lors de l\'initialization de'
                  'March\xe9Boursier: \n{}'.format(msg))
            exit()

    def request(self,
                symbole: str,
                size: str = 'compact') -> dict:
        """.

        Cette fonction envoie une requête HTTP GET à l'adresse spécifiée et
        retourne les données reçues. Retourne le cache si la requête a été
        faite récemment.

        """
        params = {
            'function': self.configurations['fonction'],
            'symbol': symbole,
            'apikey': self.configurations['apikey'],
            'outputsize': size
        }
        try:
            cache = self.__requests_cache(symbole, size)
            if cache:
                return cache
            response = requests.get(url=self.configurations['url'],
                                    params=params)
            response = json.loads(response.text)
            assert isinstance(response, dict), 'Format incorrect!'
            assert 'Error Message' not in response, response['Error Message']
        except AssertionError as msg:
            print('Une erreur est survenue lors de la requ\xeate envoy\xe9e'
                  ' \xe0 {}: \n'.format(self.configurations['url']) +
                  '\xab {} \xbb'.format(msg))
            exit()
        self.__add_to_cache(symbole, size, response)
        return response

    def __requests_cache(self, symbole: str, size: str) -> dict:
        """.

        Vérifie si la requête a déjà été faite et retourne le contenu,
        si c'est le cas. Cela évite de faire des requêtes inutiles au serveur.

        """
        if (symbole, size) in self.__req_caches and Date.dt.now() - \
                self.__req_caches[(symbole, size)]['time'] < \
                Date.timedelta(minutes=self.configurations['cache']):
            return self.__req_caches[(symbole, size)]['content']
        return None

    def __add_to_cache(self, symbole: str, size: str, contenu: dict) -> None:
        """.

        Ajoute une requête au cache pour un symbole et une "size" spécifiés.

        """
        new = {'time': Date.dt.now(), 'content': contenu}
        self.__req_caches[(symbole, size)] = new

    @staticmethod
    def __fermeture(donnees: dict, date: Date.dt.date) -> dict:
        try:
            assert 'Time Series (Daily)' in donnees, 'Format de données ' \
                                                     'inattendu:\n' \
                                                     '{}'.format(donnees)
            contenu = donnees['Time Series (Daily)'].items()
            return {k: v['4. close'] for k, v in contenu
                    if Date.std(k) <= date}
        except AssertionError as msg:
            print('Une erreur s\'est produite lors du formatage des donn\xe9es'
                  ' re\xe7ues:\n \xab {} \xbb'.format(msg))
            exit()

    @staticmethod
    def __latest_value(date: Date.dt.date, content: dict) -> float:
        key = Date.dts(date)
        if key not in content:
            if date < Date.std(list(content)[0]):
                raise ErreurDate('Date pr\xe9c\xe9dant l\'historique '
                                 'disponible: {}'.format(date))
            day = date
            while key not in content:
                day = day - Date.timedelta(days=1)
                key = Date.dts(day)
        return float(content[key])

    def prix(self, symbole: str, date: Date.dt.date) -> float:
        """.

        Cette méthode retourne le prix de fermeture du symbole boursier (en $)
        à la date spécifiée. Autrement elle retourne la valeur de fermeture la
        plus récente qui précède la date spécifiée. Pour la date du jour, si la
        bourse est présentement en activité, la valeur la plus récente
        disponible est retournée. Si aucune date n'est spécifiée elle retourne
        la valeur de fermeture la plus récente.

        """
        try:
            period = Date.period(None, Date.valider_date(date))
            size = 'compact' if period['latence'] < 100 else 'full'
            request = self.request(symbole, size)
            content = self.__fermeture(request, date)
            return self.__latest_value(date, content)
        except AssertionError as msg:
            print('Une erreur est survenue lors de l\'extraction du prix:\n'
                  '{}'.format(msg))
