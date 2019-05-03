"""Utiliser pour obtenir des données du marché boursier"""

import json
from datetime import date as dt
from datetime import timedelta as td
import datetime as datet
import requests


class ErreurDate(Exception):
    """Raise lorsque le date donnée est dans le futur"""
    pass


class MarchéBoursier:
    """Permet de stocker les prix de fermeture pour des symboles donnés"""

    try:
        with open("stock_data.txt", 'r') as file:
            dict_val = json.load(file)
    except FileNotFoundError:
        with open("stock_data.txt", 'w') as file:
            json.dump({"sample": 1}, file)
        dict_val = {}

    @staticmethod
    def date_verif(date, arg=0):
        """Sert à verifier si la date est avant ou après la date du jour :
        arg=0 pour vérifier que la date est avant la date du jour
        arg=1 pour vérifier que la date est après la date du jour
        default args=0"""

        if (arg == 0 and date > dt.today()) or (arg == 1 and date < dt.today()):
            raise ErreurDate

    def main(self, symb):
        """Permet d'ajouter les prix de fermetures au dictionnaire pour un symbole donné"""

        fonct = 'Time Series (Daily)'
        url = 'https://www.alphavantage.co/query'
        apikey = 'H3MKT1URKOMULTUZ'
        params = {'function': 'TIME_SERIES_DAILY',
                  'symbol': symb,
                  'apikey': apikey,
                  'outputsize': 'full'
                 }
        resp = json.loads((requests.get(url=url, params=params)).content)
        if not resp:
            raise ValueError('Auncune information disponible pour ce symbole.')
        try:
            self.dict_val[symb]
        except KeyError:
            self.dict_val[symb] = {d: resp[fonct][str(d)]['4. close'] for d in resp[fonct]}
        if str(dt.today()) in self.dict_val[symb] and datet.datetime.now().time() < datet.time(16):
            del self.dict_val[symb][str(dt.today())]
        with open("stock_data.txt", 'w') as file:
            json.dump(self.dict_val, file, sort_keys=True)


    def prix(self, symbole, date):
        """Retourne le prix de fermeture d'un symbole à une date donnée ou à la date précédente
        la plus proche"""
        if date > dt.today():
            raise ErreurDate
        try:
            return float(self.dict_val[symbole][str(date)])
        except KeyError:
            try:
                self.dict_val[symbole]
            except KeyError:
                self.main(symbole)
                self.prix(symbole, date)
            if date == dt.today() and datet.datetime.now().time() > datet.time(16) \
                    and str(dt.today()) not in self.dict_val[symbole]:
                del self.dict_val[symbole]
                self.main(symbole)
            i = 0
            d = date - td(days=1)
            while True:
                try:
                    if i > 15:  # Si la date < la dernière date dans les données existantes
                        raise ErreurDate("Pas de données pour {} ou avant "
                                         "pour le symbole  {}.".format(str(date), symbole))
                    return float(self.dict_val[symbole][str(d)])
                except KeyError:
                    pass
                finally:
                    d -= td(days=1)
                    i += 1
