""".

Ce module sert à fournir des outils génériques tel que la gestion de dates et
de fichiers.

Ce projet est conçu dans le cadre du cours GLO-1901.
Conçu par : Junior Cortentbach, Nguyễn Huy Dũng et René Chenard
Présenté à : Marc Parizeau

"""

import os
import json
from datetime import timedelta, datetime as dt


class ErreurDate(Exception):
    """Cette exception correspond à une date invalide."""

    pass


class Date:
    """Cette classe sert à gérer les dates et leur format."""
    dt = dt
    timedelta = timedelta

    @staticmethod
    def std(date: str) -> dt.date:
        """.

        Cette méthode (string to date) extrait la date d'un string de diverses
        formats (ex.: "AAAA-M-J", "AAAA-MM-JJ", "AAAA/MM/JJ" ou "AAAA MM JJ")
        et retourne un objet de type datetime.date.

        """
        try:
            if not date:
                return None
            chiffres = tuple(map(int, date.split('-')))
            assert len(chiffres) == 3 and chiffres, 'Date de format incorrect'\
                                                    ': {}'.format(date)
            return dt(*chiffres[:3]).date()
        except AssertionError as msg:
            print('Une erreur est survenue lors de la conversion de la date:\n'
                  '{}'.format(msg))
            exit()

    @staticmethod
    def dts(date: dt.date) -> str:
        """.

        Cette méthode prend une date de type datetime.date et retourne une
        string de format "AAAA-MM-JJ".

        """
        return date.strftime('%Y-%m-%d')

    @staticmethod
    def uniform(date: str) -> str:
        """.

        Cette méthode uniformise la date d'un string au format "AAAA-MM-JJ".

        """
        return Date.dts(Date.std(date))

    @staticmethod
    def period(debut: dt.date, fin: dt.date) -> dict:
        """.

        Cette méthode retourne la période à traiter
        sous forme d'un tuple contenant:
        1- la date de début;
        2- la date de fin;
        3- l'étendu de la période en jours;
        4- l'éloignement de la période traitée (>100jours?)

        """
        try:
            delta = (fin - debut).days if debut else None
            latence = (dt.now().date() - fin).days
        except ValueError:
            print('Le format de ces dates pose probl\xe8me:'
                  '(d\xe9but: {}) (fin: {})\n'.format(debut, fin) +
                  'Format requis: AAAA-MM-JJ (exemple: 2018-12-31)')
            exit()
        return {'debut': debut, 'fin': fin, 'delta': delta, 'latence': latence}

    @staticmethod
    def valider_date(date: dt.date) -> dt.date:
        """.

        Valide la date. Si la date n'est pas définie, retourne la date du jour.

        """
        if not date:
            return dt.today().date()
        if date > dt.today().date():
            raise ErreurDate('Les dates futures ne peuvent \xeatre'
                             ' trait\xe9es!')
        return date


class Data:
    """.

    Cette classe sert à gérer l'entreposage des données dans des fichiers JSON.

    """
    def __init__(self, fichier: str, dossier: str) -> None:
        """.

        Initialise la classe Data en s'assurant qu'un fichier au nom spécifié
        existe dans le document spécifié. Si ce n'est pas le cas, il les crée.

        """
        self.fichier = fichier
        self.dossier = dossier
        self.__location = '{}/{}'.format(dossier, fichier)
        if not os.path.exists(dossier):
            os.makedirs(dossier)
        if not os.path.isfile(self.__location):
            self.write()

    def read(self) -> dict:
        """.

        Retourne le contenu du fichier JSON.

        """
        try:
            with open(self.__location, 'r') as file:
                content = json.load(file)
            return content
        except json.decoder.JSONDecodeError:
            self.__replace_erroneous()
            return self.read()

    def write(self, content: dict = None) -> None:
        """.

        Écrit le contenu spécifié dans le fichier JSON.

        """
        content = content if content else {}
        with open(self.__location, 'w') as file:
            json.dump(content, file)

    def __replace_erroneous(self) -> None:
        """.

        Renomme le fichier existant s'il n'est pas du bon format.

        """
        while os.path.isfile(self.__location):
            os.rename(self.__location, '{}.bak'.format(self.__location))
        print("Un fichier au même nom que {} se trouvait déjà dans le dossier"
              " {}, il a été renommé {}.".format(
                  self.fichier, self.dossier, '{}.bak'.format(self.fichier)))
        self.write()

    def get_value(self, key: str) -> object:
        """.

        Retourne une valeur entreposée dans le fichier JSON.

        """
        content = self.read()
        if key not in content:
            return None
        return content[key]

    def set_value(self, key: str, value: object) -> None:
        """.

        Entrepose une valeur dans le fichier JSON.

        """
        content = self.read()
        content[key] = value
        self.write(content)

    def update_value(self, key: str, value: object) -> None:
        """.

        Met à jour une la valeur d'une clé.

        """
        content = self.read()
        if isinstance(content[key], dict):
            content[key].update(value)
        elif isinstance(content[key], list):
            content[key] += value
        else:
            content[key] = value
        self.write(content)

    def get_or_set(self, key: str, value: object) -> object:
        """.

        Retourne la valeur si elle est déjà établie, sinon établi la valeur.

        """
        val = self.get_value(key)
        if not val:
            self.set_value(key, value)
        return val
