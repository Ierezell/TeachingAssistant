import argparse
import datetime
import json
import requests

today = datetime.date.isoformat(datetime.date.today())  # on définit immédiatement la variable pour l'arguement
# par défaut de la date de fin

parser = argparse.ArgumentParser("Extraction de valeurs historiques pour un symbole boursier")
parser.add_argument("symbol", metavar="symbol", nargs="+", help="Nom du symbole boursier désiré")
parser.add_argument("-f", "--fin", metavar="DATE", dest="date_fin", default=today,
                    help="Date recherchée la plus récente (format: AAAA-MM-JJ)")

arguments = parser.parse_args('--fin')  # on passe immédiatement des arguments afin d'indiquer facilement la valeur
# par défaut de la date initial. et on continue d'ajouter des arguments.

parser.add_argument("-d", "--début", metavar="DATE", dest="date_ini", default=arguments.date_fin,
                    help="Date recherchée la plus ancienne (format: AAAA-MM-JJ)")
parser.add_argument("-v", "--valeur", metavar="{fermeture,ouverture,min,max,volume}",
                    choices=["fermeture", "ouverture", "min", "max", "volume"],
                    dest="choix_valeur", default="fermeture", help="La valeur désirée (par défaut: fermeture)")

arguments = parser.parse_args() # on passe les arguments au programme

# on s'assure que les dates sont dans le bon format. Pour ce faire, on les converties en objets datetime qui reconnais
#  le format de date YYYY-M-J autant que YYYY-MM-JJ. On convertie ensuite l'objet en string avec le format désiré
arguments.date_ini = datetime.datetime.strftime(datetime.datetime.strptime(arguments.date_ini,'%Y-%m-%d'),'%Y-%m-%d')
arguments.date_fin = datetime.datetime.strftime(datetime.datetime.strptime(arguments.date_fin,'%Y-%m-%d'),'%Y-%m-%d')


# fonction qui ne fait que s'appoprier les infos demandées sur le serveur du site ciblé.
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

    return response # toutes les informations sont stockées dans ce dictionnaire


# Définition d'une nouvelle classe qui contiendra de manière claire toutes les informations demandées par l'utilisateur
class InfosDemandes:

    def __init__(self, symbol):
        self.biblio = obtenir_infos(symbol)
        self.date_debut = arguments.date_ini
        self.date_fin = arguments.date_fin
        self.variable = arguments.choix_valeur

    def indice_boursiers(self):

        return self.biblio['Meta Data']['2. Symbol']

    def valeur_demandé(self):
        nom_paramètre = {'fermeture': '4. close', 'ouverture': '1. open', 'min': '3. low', 'max': '2. high',
                           'volume': '5. volume'}
        liste = [(self.date_debut, self.biblio["Time Series (Daily)"][self.date_debut][nom_paramètre[self.variable]])
            , (self.date_fin, self.biblio["Time Series (Daily)"][self.date_fin][nom_paramètre[self.variable]])]

        return sorted(list(set(liste)))


for i in arguments.symbol:
    infos = InfosDemandes(i)

    print('{}({}, {}, {})'.format(infos.indice_boursiers(), infos.variable, infos.date_debut, infos.date_fin))
    print(infos.valeur_demandé())
    print()  # ajout d'un espace final pour plus de clareté lors de multiple requêtes
