"""Utiliser pour se créer un portefeuille d'actions"""

from collections import defaultdict as ddict
from datetime import date as dt
import datetime as datet
import marche_boursier as marche_bour



class LiquiditéInsuffisante(Exception):
    """Raise cette exeception lorsque les fonds sont insuffisants"""
    pass


class ErreurQuantité(Exception):
    """Raise quand la quantité demandée est erronée"""
    pass


class Portefeuille:
    """Permet de conserver toutes les données reliées à la bourse dans ce portefeuille d'actions"""

    def __init__(self, instance_marche=marche_bour.MarchéBoursier()):
        self.ide = instance_marche
        self.transactions = ddict(lambda: 0.0, {})
        self.actions = ddict(lambda: ddict(lambda: 0.0, {}), {})

    def déposer(self, montant, date=dt.today()):
        """Ajoute le montant donné au dictionnaire de transactions à la date donnée"""

        marche_bour.MarchéBoursier().date_verif(date)
        self.transactions[str(date)] += montant


    def solde(self, date=dt.today()):
        """Retourne la somme de toutes les transactions jusqu'à une date donnée"""

        marche_bour.MarchéBoursier().date_verif(date)

        return sum([x[1] for x in filter(
            lambda x: datet.datetime.strptime(x[0], '%Y-%m-%d').date() <= date, self.transactions.items())], 0.0)


    def symboles(self, date):
        """Retourne une liste des symboles transigés dans le portefeuille"""
        date = datet.datetime.strptime(str(date), '%Y-%m-%d').date()
        try:
            datei = datet.datetime.strptime(sorted(self.transactions.keys())[0], '%Y-%m-%d').date()
        except IndexError:
            datei = dt.today()
        liste_keys = []
        while date >= datei:
            if not self.actions[str(date)]:
                date -= marche_bour.td(days=1)
            else:
                liste_keys += list(self.actions[str(date)].keys())
                date -= marche_bour.td(days=1)
        return list(set(liste_keys))

    def acheter(self, symbole, quantite, date=dt.today()):
        """Ajoute la quantité d'actions désirée au dictionnaire d'actions et
        ajoute une transaction dans le dictionnaire de transactions"""

        montant = quantite * self.ide.prix(symbole, date)
        marche_bour.MarchéBoursier().date_verif(date)
        if self.solde(date) < montant or self.solde() < montant:
            raise LiquiditéInsuffisante
        self.actions[str(date)][symbole] += quantite
        self.déposer(-montant, date)

    def vendre(self, symbole, quantite, date=dt.today()):
        """Retire la quantité d'actions pour un symbole au dictionnaire d'actions et
        ajoute une transaction dans le dictionnaire de transactions"""

        marche_bour.MarchéBoursier().date_verif(date)
        if self.nb_actions(date)[symbole] < quantite or self.nb_actions()[symbole] < quantite:
            raise ErreurQuantité
        self.actions[str(date)][symbole] -= quantite
        self.déposer(quantite * self.ide.prix(symbole, date), date)

    def nb_actions(self, date=dt.today()):
        """Retourne un dictionnaire avec le nombre de chaque action du
        portefeuille pour une date donnée"""

        marche_bour.MarchéBoursier().date_verif(date)
        if not self.actions:
            return {}
        nb_actions = {}
        for symbole in self.symboles(date):
            action_par_symbole = 0
            d = datet.datetime.strptime(sorted(list(self.actions))[0], '%Y-%m-%d').date()
            while d <= date:
                action_par_symbole += self.actions[str(d)][symbole]
                d += marche_bour.td(days=1)
            if action_par_symbole != 0:
                nb_actions[symbole] = action_par_symbole
        return ddict(lambda: 0.0, nb_actions)

    def titres(self, date=dt.today()):
        """Retourne les titres sous le bon format en dict"""

        return dict(self.nb_actions(date))

    def valeur_totale(self, date=dt.today()):
        """Retourne la valeur totale du portefeuille à une date donnée"""

        marche_bour.MarchéBoursier().date_verif(date)
        valeur_tot = self.solde(date)
        for symbole in self.nb_actions(date):
            valeur_tot += self.nb_actions(date)[symbole] * self.ide.prix(symbole, date)
        return valeur_tot

    def val_titres(self, symboles, date=dt.today()):
        """Retourne la valeur de toutes les actions à la date donnée"""

        marche_bour.MarchéBoursier().date_verif(date)
        val_titres = 0.0
        for symbole in symboles:
            val_titres += self.nb_actions(date)[symbole] * self.ide.prix(symbole, date)
        return val_titres
