""".

Ce module contient une fonctionnalité principale: gérer un portefeuille
d'actions à la bourse.

Ce script requiert que les modules `outils` et `marche_boursier` développés
dans le cadre du même projet.

Ce projet est conçu dans le cadre du cours GLO-1901.
Conçu par : Junior Cortentbach, Nguyễn Huy Dũng et René Chenard
Présenté à : Marc Parizeau

"""

from datetime import timedelta as td
from outils import Date
from marche_boursier import MarchéBoursier

class ErreurQuantité(Exception):
    """.

    Cette exception correspond à une quantité invalide. En particulier,
    lorsqu'il n'y a pas suffisamment de d'actions pour completer la
    transaction.

    """

    pass


class LiquiditéInsuffisante(Exception):
    """.

    Cette exception est soulevée lorsqu'il n'y a pas suffisamment de liquidités
    pour completer la transaction.

    """

    pass


class Portefeuille:
    """.

    Cette classe sert essentiellement à gérer un portefeuille d'actions à la
    bourse.

    """

    def __init__(self, m_b: MarchéBoursier = None, *, load=None):
        """.

        Un constructeur qui accepte une instance de la classe MarchéBoursier et
        qui effectue les initialisations qui s'imposent.

        """
        try:
            if load:
                assert 'journal' in load
                assert 'fonds' in load
                assert 'actions' in load
            self.marche_bourse = m_b if m_b else MarchéBoursier()
            self.journal = load['journal'] if load else {}
            self.__registre_fonds = load['fonds'] if load else {}
            self.__registre_actions = load['actions'] if load else {}
        except AssertionError as msg:
            print('Une erreur est survenue lors de l\'initialisation du '
                  'portefeuille:\n{}'.format(msg))

    def rapport(self, option: iter = None) -> dict:
        """.

        Cette méthode retourne un rapport des activités du portefeuille.

        """
        rapport_complet = {'fonds': self.__registre_fonds,
                           'actions': self.__registre_actions,
                           'journal': self.journal}
        if option and option in rapport_complet:
            return rapport_complet[option]
        return rapport_complet

    def déposer(self,
                montant: float,
                date: Date.dt.date = None) -> str:
        """.

        Cette méthode effectue le dépôt du montant liquide dans le portefeuille
        à la date spécifiée. Si aucune date n'est spécifiée, la méthode
        utilisera la date du jour.

        """
        date = Date.valider_date(date)
        if Date.dts(date) not in self.__registre_fonds:
            self.__registre_fonds[Date.dts(date)] = 0
        self.__registre_fonds[Date.dts(date)] += montant
        acte = 'D\xe9p\xf4t de {}$. Solde: {}$'.format(
            round(montant, 2), round(self.solde(date), 2))
        self.__ajouter_au_journal(date, acte)
        return acte

    def solde(self, date: Date.dt.date = None) -> float:
        """.

        Cette méthode retourne le solde des liquidités du portefeuile à la date
        spécifiée. Si aucune date n'est spécifiée, la méthode utilisera la date
        du jour.

        """
        date = Date.valider_date(date)
        return sum([val for key, val in self.__registre_fonds.items() if
                    Date.std(key) <= date])

    def acheter(self,
                symbole: str,
                quantité: float,
                date: Date.dt.date = None) -> str:
        """.

        Cette méthode effectue l'achat de la quantité d'actions du titre
        symbole à la date spécifiée. Si aucune date n'est spécifiée, la méthode
        utilisera la date du jour. Avant d'effectuer cette transaction, la
        méthode s'assure que le portefeuille contient suffisamment de
        liquidités à la date spécifiée pour acheter la quantité désirée de ce
        titre au prix du marché.

        """
        symbole = symbole.lower()
        date = Date.valider_date(date)
        prix = self.marche_bourse.prix(symbole, date)
        montant = quantité * prix
        if self.__valider_solde(montant, date):
            if Date.dts(date) not in self.__registre_fonds:
                self.__registre_fonds[Date.dts(date)] = 0
            self.__registre_fonds[Date.dts(date)] -= montant
            if symbole not in self.__registre_actions:
                self.__registre_actions[symbole] = {}
            if Date.dts(date) not in self.__registre_actions[symbole]:
                self.__registre_actions[symbole][Date.dts(date)] = 0
            self.__registre_actions[symbole][Date.dts(date)] += quantité
            total = self.titres(date)[symbole]
            acte = 'Achat de {} actions de {} au prix de {}$ par' \
                   ' action. Total: {}'.format(round(quantité, 2),
                                               symbole.upper(),
                                               round(prix, 2),
                                               round(total, 2))
            self.__ajouter_au_journal(date, acte)
        return acte

    def vendre(self,
               symbole: str,
               quantité: float,
               date: Date.dt.date = None) -> str:
        """.

        Cette méthode effectue une vente de la quantité d'action du titre du
        symbole à la date spécifiée. Si aucune date n'est spécifiée, la méthode
        utilisera la date du jour. Avant de procéder à cette transaction, la
        méthode s'assure que le portefeuille possède bien à la date spécifiée
        suffisamment d'actions de ce titre pour pouvoir compléter la vente.
        Le fruit de la vente au prix du marché à la date spécifiée est déposé
        sous forme liquide dans le portefeuille.

        """
        symbole = symbole.lower()
        date = Date.valider_date(date)
        if self.__valider_quant(quantité, symbole, date):
            prix = self.marche_bourse.prix(symbole, date)
            montant = quantité * prix
            if Date.dts(date) not in self.__registre_actions[symbole]:
                self.__registre_actions[symbole][Date.dts(date)] = 0
            self.__registre_actions[symbole][Date.dts(date)] -= quantité
            if Date.dts(date) not in self.__registre_fonds:
                self.__registre_fonds[Date.dts(date)] = 0
            self.__registre_fonds[Date.dts(date)] += montant
            total = self.titres(date)[symbole]
            acte = 'Vente de {} actions de {} au prix de {}$ par' \
                   ' action. Total: {}'.format(round(quantité, 2),
                                               symbole.upper(),
                                               round(prix, 2),
                                               round(total, 2))
            self.__ajouter_au_journal(date, acte)
        return acte

    def valeur_totale(self, date: Date.dt.date = None) -> float:
        """.

        Cette méthode retourne la valeur totale du portefeuille à cette date,
        c'est-à-dire la somme des liquidités et des valeurs de tous les titres
        du portefeuille à la date spécifiée. Si aucune date n'est spécifiée, la
        méthode utilisera la date du jour.

        """
        date = Date.valider_date(date)
        titres = self.valeur_des_titres(self.titres(date).keys(), date)
        fonds = self.solde(date)
        return titres + fonds

    def valeur_des_titres(self,
                          symboles: iter = None,
                          date: Date.dt.date = None) -> float:
        """.

        Cette méthode retourne pour la date spécifiée la valeur totale des
        titres correspondants. Si aucune date n'est spécifiée, la méthode
        utilisera la date du jour. Si aucun titre n'est spécifié, la méthode
        retourne la valeur de l'ensemble des titres détenus.

        """
        date = Date.valider_date(date)
        symboles = symboles if symboles else self.titres(date).keys()
        valeur = 0
        for symbole in symboles:
            if symbole not in self.titres():
                continue
            symbole = symbole.lower()
            quantité = self.titres(date)[symbole]
            prix = self.marche_bourse.prix(symbole, date)
            valeur += quantité * prix
        return valeur

    def titres(self, date: Date.dt.date = None) -> dict:
        """.

        Cette méthode retourne pour la date spécifiée en argument, un
        dictionnaire des symboles de tous les titres du portefeuille à cette
        date, avec les quantités d'actions détenues pour ces titres. Si aucune
        date n'est spécifiée, la méthode utilisera la date du jour.

        """
        date = Date.valider_date(date)
        ensemble = {}
        for symbole, liste in self.__registre_actions.items():
            ens = [val for key, val in liste.items() if Date.std(key) <= date]
            ensemble[symbole] = sum(ens)
        return ensemble

    def valeur_projetée(self, date: Date.dt.date, rendement: dict) -> float:
        u""".

        Cette méthode projette la valeur du portefeuille à cette date en
        supposant le ou les rendements spécifiés. L'argument rendement peut ici
        prendre deux formes. Soit un rendement fixe (float) applicable à tous
        les titres du portefeuille, soit un dictionnaire de rendements
        associés à des titres spécifiques (via leur symbole). Dans le second
        cas, si le portefeuille contient des titres pour lesquels aucun
        rendement n'est précisé dans le dictionnaire, alors la méthode doit
        supposer que le rendement est nul. De même, le rendement des
        liquidités est supposé nul.

        """

        def annee_jour_partiel(jour):
            u"""

                Cette méthode retourne le nombre d'années et
                le nombres de jours partielle.

            """
            annees = int(Date.period(today, jour)['delta'] / 365)
            jour_de_annee_partielle = Date.period(today, jour)['delta'] - 365 * annees
            return (annees, jour_de_annee_partielle)

        today = Date.dt.today().date()
        nb_jours_a_calculer = int(Date.period(today, date)['delta'] / 90) + 2
        liste_jours_a_calculer = [today + td(min(90 * i, Date.period(today, date)['delta'])) for i
                                  in range(nb_jours_a_calculer)]
        total = [self.solde(today)] * nb_jours_a_calculer

        rend = {sym: rendement[sym] for sym in rendement}

        for symbole, actions in self.titres(today).items():
            if symbole in rend:
                prix = self.marche_bourse.prix(symbole, today)
                for i in range(nb_jours_a_calculer):
                    total[i] += prix * actions * (1 + rend[symbole]) ** \
                                annee_jour_partiel(liste_jours_a_calculer[i])[0] + \
                                annee_jour_partiel(liste_jours_a_calculer[i])[1] / 365 * prix * \
                                actions * rend[symbole]
        dict_dates_et_valeurs = {liste_jours_a_calculer[i]: total[i] for i in
                                 range(nb_jours_a_calculer)}
        return dict_dates_et_valeurs

    def __valider_solde(self, montant: float, date: Date.dt.date) -> bool:
        différence = self.solde(date) - montant
        if différence < 0:
            raise LiquiditéInsuffisante('Impossible de proc\xe9der \xe0 la '
                                        'transaction: fonds insuffisants!\n'
                                        'Il manque {}$.'.format(différence))
        return True

    def __valider_quant(self,
                        quant: float,
                        symbole: str,
                        date: Date.dt.date) -> bool:
        if quant > self.titres(date)[symbole]:
            raise ErreurQuantité('Impossible de proc\xe9der \xe0 la '
                                 'transaction: quantit\xe9 insuffisante!')
        return True

    def __ajouter_au_journal(self, date: Date.dt.date, acte: str) -> None:
        if Date.dts(date) not in self.journal:
            self.journal[Date.dts(date)] = []
        self.journal[Date.dts(date)].append(acte)
