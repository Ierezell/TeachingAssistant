import argparse
import datetime
import json
import requests

today = datetime.datetime.now()
today = today.strftime("%Y-%m-%d")  # on définit immédiatement la variable pour l'arguement par défaut de la date de fin

parser = argparse.ArgumentParser("Extraction de valeurs historiques pour un symbole boursier")
parser.add_argument("symbol", metavar="symbol", nargs="+", help="Nom du symbole boursier désiré")
parser.add_argument("-f", "--fin", metavar="DATE", dest="date_fin", default=today,
                    help="Date recherchée la plus récente (format: AAAA-MM-JJ)")

arguments = parser.parse_args('--fin')  # on passe immédiatement des arguments fin d'indiquer facilement la valeur
                                        # par defaut de la date initial

parser.add_argument("-d", "--début", metavar="DATE", dest="date_ini", default=arguments.date_fin,
                    help="Date recherchée la plus ancienne (format: AAAA-MM-JJ)")
parser.add_argument("-v", "--valeur", metavar="{fermeture,ouverture,min,max,volume}",
                    choices=["fermeture", "ouverture", "min", "max", "volume"],
                    dest="choix_valeur", default="fermeture")

arguments = parser.parse_args()


def obtenir_infos(symbol):
    url = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY'
    apikey = '3PQRLNKE9VP5JH12'

    params = {
        'function': function,
        'symbol': symbol,
        'apikey': apikey,
        'outputsize': 'compact',
    }

    response = requests.get(url=url, params=params)
    response = json.loads(response.text)

    return response


class InfosDemandes:

    def __init__(self, symbol):
        self.biblio = obtenir_infos(symbol)
        self.date_debut = arguments.date_ini
        self.date_fin = arguments.date_fin
        self.variable = arguments.choix_valeur

    def indice_boursiers(self):
        self.indice_boursier = self.biblio['Meta Data']['2. Symbol']

    def valeur_demandé(self):
        choix_de_valeur = {'fermeture': '4. close', 'ouverture': '1. open', 'min': '3. low', 'max': '2. high',
                   'volume': '5. volume'}
        liste = [(self.date_debut, self.biblio["Time Series (Daily)"][self.date_debut][choix_de_valeur[self.variable]])
            , (self.date_fin, self.biblio["Time Series (Daily)"][self.date_fin][choix_de_valeur[self.variable]])]

        self.valeurs = sorted(list(set(liste)))

    def initialiser(self):     #fonction non nécéssaire pour la classe, les valeurs aurait pu être créé en dehors de la
                                #class. Cette fonction ne sert qu'à desengorger le code
        self.indice_boursiers()
        self.valeur_demandé()


for i in arguments.symbol:
    infos = InfosDemandes(i)
    infos.initialiser()

    print('{}({}, {}, {})'.format(infos.indice_boursier,infos.variable, infos.date_debut, infos.date_fin))
    print(infos.valeurs)
    print()
