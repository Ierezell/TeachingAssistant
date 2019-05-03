"""Gestion d'un portefeuille"""

import json
import argparse
from collections import defaultdict as ddict
from datetime import date as dt
import datetime as datet
import matplotlib.pyplot as mpl
import numpy as np
import Portefeuille as pt


parser = argparse.ArgumentParser(description="Gestionnaire de portefeuille d'actions")
subparsers = parser.add_subparsers(title='ACTIONS')


class Foo:
    """Créer les arguments avec argparse"""

    def __init__(self, action, fonction, aide):
        self.parser_action = subparsers.add_parser(action, help=aide)
        self.fonction = fonction
        self.arguments()

    def arguments(self):
        """Arguments des subparsers"""
        self.parser_action.add_argument("-d", "--date",
                                        type=str,
                                        default=str(dt.today()),
                                        help="Date effective (par défaut, date du jour)")
        self.parser_action.add_argument("-q", "--quantité",
                                        type=int,
                                        default=1,
                                        metavar="INT",
                                        help="Quantité désirée (par défaut: 1)")
        self.parser_action.add_argument("-t", "--titres",
                                        metavar="STRING",
                                        nargs='+',
                                        type=str,
                                        help="Le ou les titres à considérer (par défaut, tous les "
                                        "titres du portefeuille sont considérés)")
        self.parser_action.add_argument("-r", "--rendement",
                                        type=float,
                                        default=0,
                                        metavar="FLOAT",
                                        help="Rendement annuel global (par défaut, 0)")
        self.parser_action.add_argument("-v", "--volatilité",
                                        type=float,
                                        default=0,
                                        metavar="FLOAT",
                                        help="Indice de volatilité global sur le rendement annuel (par défaut, 0)")
        self.parser_action.add_argument("-g", "--graphique",
                                        default=False,
                                        metavar="BOOL",
                                        help="Affichage graphique (par défaut, pas d'affichage graphique)")
        self.parser_action.add_argument("-p", "--portefeuille",
                                        type=str,
                                        default='folio',
                                        metavar="STRING",
                                        help="Nom de portefeuille (par défaut, utiliser folio)")
        self.parser_action.set_defaults(func=self.fonction)


def get_port_inst():
    """Retourne une instance de portefeuille"""

    return pt.Portefeuille()


def déposer():
    """Dépose quantité de le portefeuille"""

    data = ouvrir(instpor)
    instpor.déposer(ARGS.quantité, datet.datetime.strptime(ARGS.date, '%Y-%m-%d').date())
    écrire(data)


def acheter():
    """Achète des titres"""

    data = ouvrir(instpor)
    for titre in ARGS.titres:
        instpor.acheter(titre, ARGS.quantité, datet.datetime.strptime(ARGS.date, '%Y-%m-%d').date())
    écrire(data)


def vendre():
    """Vend des titres"""

    data = ouvrir(instpor)
    for titre in ARGS.titres:
        instpor.vendre(titre, ARGS.quantité, datet.datetime.strptime(ARGS.date, '%Y-%m-%d').date())
    écrire(data)

def solde():
    """Print le solde à la date"""

    ouvrir(instpor)
    print("{:.2f}".format(instpor.solde(datet.datetime.strptime(ARGS.date, '%Y-%m-%d').date())))
    if ARGS.graphique:
        x.solde()

def titres():
    """Print symbole=quantité pour tous les titres donnés du portefeuille"""

    ouvrir(instpor)
    dicttitres = instpor.titres(datet.datetime.strptime(ARGS.date, '%Y-%m-%d').date())
    for titre in ARGS.titres:
        try:
            print("{}={}".format(titre, int(dicttitres[titre])))
        except KeyError:
            print("{}={}".format(titre, 0))
    if ARGS.graphique:
        x.titres_graph()


def valeur():
    """valeur totale des titres spécifiés"""

    ouvrir(instpor)
    print("{:.2f}".format(instpor.val_titres(ARGS.titres, datet.datetime.strptime(ARGS.date, '%Y-%m-%d').date())))
    if ARGS.graphique:
        x.valeur()

def projection():
    """Projection à une date donnée"""

    ouvrir(instpor)
    date = datet.datetime.strptime(ARGS.date, '%Y-%m-%d').date()
    pt.marche_bour.MarchéBoursier().date_verif(date, 1)
    annees = (date - dt.today()).days / 365
    perc = {"25": 0, "50": 0, "75": 0}
    for titre in sorted(ARGS.titres):
        try:
            moyenne, ecart_type = dicttitres[titre][0], dicttitres[titre][1]
        except Exception:
            moyenne, ecart_type = ARGS.rendement, ARGS.volatilité
        rendements = np.random.normal(moyenne, ecart_type, 10000)
        val = instpor.val_titres([titre])
        liste = []
        for rend in rendements:
            liste.append(val*(1 + rend)**annees)
        arr = np.array(liste)
        for i in perc:
            perc[i] += np.percentile(arr, int(i))
    print(tuple([round(i, 2) for i in perc.values()]))
    if ARGS.graphique:
        x.projection()

def proj(date):
    """Projection pour graphique"""

    annees = (date - dt.today()).days / 365
    perc = {"25": 0, "50": 0, "75": 0}
    for titre in sorted(ARGS.titres):
        try:
            moyenne, ecart_type = dicttitres[titre][0], dicttitres[titre][1]
        except Exception:
            moyenne, ecart_type = ARGS.rendement, ARGS.volatilité
        rendements = np.random.normal(moyenne, ecart_type, 10000)
        val = instpor.val_titres([titre])
        liste = []
        for rend in rendements:
            liste.append(val * (1 + rend) ** annees)
        arr = np.array(liste)
        for i in perc:
            perc[i] += np.percentile(arr, int(i))
    return tuple([round(i, 2) for i in perc.values()])


class PortefeuilleGraphique(pt.Portefeuille):
    """graph"""

    def __init__(self):
        super().__init__()
        ouvrir(self)
        try:
            self.date = datet.datetime.strptime(sorted(self.transactions.keys())[0], '%Y-%m-%d').date()
        except IndexError:
            self.data = dt.today()

    def solde(self):
        """Grapqhique du solde"""

        liste_solde = []
        list_date = []
        while self.date <= dt.today():
            list_date.append(self.date)
            liste_solde.append(super().solde(self.date))
            self.date += datet.timedelta(days=1)
        mpl.plot(list_date, liste_solde, '-r', label='solde')
        mpl.xticks(rotation=30)
        mpl.title("Solde du portefeuille en dollars en fonction de la date")
        mpl.legend()
        mpl.xlabel("Date")
        mpl.ylabel("Dollars $")
        mpl.grid(True)
        mpl.show()

    def titres_graph(self):
        """Grapqhique des titres"""

        list_nb_action = []
        list_date = []
        for titre in ARGS.titres:
            d = self.date
            x = []
            while d <= dt.today():
                list_date.append(d)
                x.append(super().nb_actions(d)[titre])
                d += datet.timedelta(days=1)
            list_nb_action.append(x)
        list_date = sorted(list(set(list_date)))
        i = 0
        couleur = ['r', '--b', '-.g', ':y', '-c', '2m', '-..k']
        for titre in ARGS.titres:
            mpl.plot(list_date, list_nb_action[i], couleur[i], label=titre)
            if i == 7:
                i = 0
            else:
                i += 1
        mpl.xticks(rotation=30)
        mpl.title("Titres du portefeuille en fonction de la date")
        mpl.legend()
        mpl.xlabel("Date")
        mpl.ylabel("Nombre d'actions")
        mpl.grid(True)
        mpl.show()

    def valeur(self):
        """Graphique de la valeur totale"""

        liste_date = []
        valeur_tot = []
        while self.date <= dt.today():
            liste_date.append(self.date)
            valeur_tot.append(super().val_titres(ARGS.titres, self.date))
            self.date += datet.timedelta(days=1)

        mpl.plot(liste_date, valeur_tot, '-r', label='Valeur totale')
        mpl.xticks(rotation=30)
        mpl.title("Valeur des titres du portefeuille en dollars en fonction de la date")
        mpl.legend()
        mpl.xlabel("Date")
        mpl.ylabel("Valeur totale")
        mpl.grid(True)
        mpl.show()

    def projection(self):
        """Graphique de la projection"""

        liste_date = []
        quart_25 = []
        quart_50 = []
        quart_75 = []
        self.date = dt.today()
        while self.date <= datet.datetime.strptime(ARGS.date, '%Y-%m-%d').date():
            tuples = proj(self.date)
            liste_date.append(self.date)
            quart_25.append(tuples[0])
            quart_50.append(tuples[1])
            quart_75.append(tuples[2])
            self.date += datet.timedelta(weeks=12)

        mpl.plot(liste_date, quart_25, '-r', label='Q25')
        mpl.plot(liste_date, quart_50, '--b', label='Q50')
        mpl.plot(liste_date, quart_75, '-.g', label='Q75')
        mpl.xticks(rotation=30)
        mpl.title("Valeur des quartiles des projections en fonction de la date")
        mpl.legend()
        mpl.xlabel("Date")
        mpl.ylabel("Dollars")
        mpl.grid(True)
        mpl.show()

#Subparsers
Foo('déposer', déposer, "Déposer la quantité de dollars spécifiée, à la date spécifiée")
Foo("acheter", acheter, "Acheter la quantité spécifiée des titres spécifiés, à la date spécifiée")
Foo("vendre", vendre, "Vendre la quantité spécifiée des titres spécifiés, à la date spécifiée")
Foo("solde", solde, "Afficher en dollars le solde des liquidités, à la date spécifiée")
Foo("titres", titres, "Afficher les nombres d'actions détenues "
                      "pour chacun des titres spécifiés, à la date spécifiée; "
                      "affichez une ligne par titre, avec le format titre=quantité")
Foo("valeur", valeur, "Afficher la valeur totale des titres spécifiés, "
                      "à la date spécifiée; affichez la valeur sur une ligne, "
                      "en limitant l'affichage à 2 décimales")
Foo("projection", projection, "Projeter la valeur totale des titres spécifiés, "
                              "à la date future spécifiée, en tenant compte des rendements "
                              "et indices de volatilité spécifiés; affichez la projection sur une seule ligne, "
                              "en limitant l'affichage de la valeur à 2 décimales")
ARGS = parser.parse_args()

dicttitres = {}
try:
    for shit in ARGS.titres:
        x = shit.split('(')[0]
        try:
            y = list(map(float, shit.split('(')[1].rstrip(')').split(',')))
        except IndexError:
            y = None
        finally:
            dicttitres[x] = y
except TypeError:
    pass
ARGS.titres = list(dicttitres.keys())
instpor = get_port_inst()


def ouvrir(instance):
    """Aller charcher les données et les asignées"""
    try:
        with open(ARGS.portefeuille, 'r') as file:
            data = json.load(file)
        instance.transactions = ddict(lambda: 0.0, data["transactions"])
        instance.actions = ddict(lambda: ddict(lambda: 0.0, {}), data["actions"])
        for date in instance.actions:
            instance.actions[date] = ddict(lambda: 0.0, data["actions"][date])
        if not ARGS.titres:
            ARGS.titres = instance.symboles(ARGS.date)
        return data
    except FileNotFoundError:
        with open(ARGS.portefeuille, 'w') as file:
            json.dump({'transactions': {},
                       'actions': {}
                      }, file)
        return ouvrir(instance)


def écrire(data):
    """Écrire les données dans le file"""

    data["transactions"] = instpor.transactions
    data["actions"] = instpor.actions
    with open(ARGS.portefeuille, 'w') as file:
        json.dump(data, file, indent=1, sort_keys=True)
x = PortefeuilleGraphique()
ARGS.func()
