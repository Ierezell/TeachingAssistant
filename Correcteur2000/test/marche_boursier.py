""""Classe MarchéBoursier"""
import datetime
import json
import requests


class ErreurDate(Exception):
    """Erreur de type ErreurDate"""


class MarchéBoursier:
    """Classe MarchéBoursier"""
    @staticmethod
    def prix(symbole, date):
        """Retourne la valeur de fermeture d'un titre à la date spécifiée"""
        url = f'https://python.gel.ulaval.ca/action/{symbole}/historique'
        aujourdhui = datetime.date.today()
        un_jour = datetime.timedelta(days=1)

        if date == aujourdhui:
            date -= un_jour
        elif (date - aujourdhui) >= un_jour:
            raise ErreurDate('''La date doit être égale ou ultérieure à la date d'aujourd'hui''')

        params = {
            'début': date,
            'fin': date,
        }
        response = requests.get(url=url, params=params)
        response = json.loads(response.text)

        for _ in range(7):
            if len(response['historique']) == 1:
                price = response['historique'][str(date)]['fermeture']
                break
            else:
                date -= un_jour
                params = {
                    'début': date,
                    'fin': date,
                }
                response = requests.get(url=url, params=params)
                response = json.loads(response.text)
        return price
