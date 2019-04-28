'''Classe Portefeuille'''
import datetime
from marche_boursier import ErreurDate


class LiquiditéInsuffisante(Exception):
    """Erreur de type LiquiditéInsuffisante"""


class ErreurQuantité(Exception):
    """Erreur de type ErreurQuantité"""


class Portefeuille:
    """Classe Portefeuille: Permet de gérer un portefeuille boursier"""
    def __init__(self, marché):
        """Initialise le portefeuille boursier"""
        self.marché = marché
        self.dépots = {}  # Dictionnaire contenant les dépôts et retraits (dépots négatifs)
        # effectués aux dates correspondantes
        self.achats = {}  # Dictionnaire contenant les titres achetés. Garde en mémoire toutes
        # les achats effectués.
        self.ventes = {}  # Dictionnaire contenant les titres vendus. Garde en mémoire toutes
        # les ventes.

    def déposer(self, montant, date=datetime.date.today()):
        """Ajoute de l'argent au portefeuille à la date spécifiée"""
        if date > datetime.date.today():
            raise ErreurDate('''La date doit être postérieure à la date d'aujourd'hui''')
        if self.dépots.get(date) is None:  # Aucun dépôt effectué cette journée là pour l'instant
            self.dépots[date] = [montant]
        else:  # Il y a déjà eu un dépôt durant la journée
            self.dépots[date].append(montant)

    def solde(self, date=datetime.date.today()):
        """Calcule le solde dans le portefeuille à la date spécifiée"""
        if date > datetime.date.today():
            raise ErreurDate('''La date ne peut être ultérieure
             à la date d'aujourd'hui''')
        solde = 0
        for date_dépot, montant in self.dépots.items():  # Parcour toutes les dates où
            # il y a eu un dépôt
            if date_dépot <= date:  # Comptabilise seulement celle avant la date spécifiée
                solde += sum(montant)
        return solde

    def acheter(self, symbole, quantite, date=datetime.date.today()):
        """Permet d'ajouter des titres à ceux déjà possédés"""
        if date > datetime.date.today():
            raise ErreurDate('''La date ne peut être ultérieure à la date d'aujourd'hui''')
        price = quantite * self.marché.prix(symbole, date)
        if self.solde(date) < price:  # Vérification des liquidités
            raise LiquiditéInsuffisante('''Impossible d'effectuer l'achat, les
             liquidités sont insuffisantes''')
        if self.achats.get(date) is None:  # Il n'y a pas encore eu d'achat à cette date
            self.achats[date] = {symbole: quantite}
        elif self.achats[date].get(symbole) is None:  # Il n'y a pas encore eu d'achat de
            # ce titre à cette date
            self.achats[date][symbole] = quantite
        else:  # Il y a déja eu achat de ce titre à cette date
            self.achats[date][symbole] += quantite
        self.déposer(-price, date)

    def titres(self, date=datetime.date.today()):
        """Retourne les titres possédés à la date spécifiée"""
        if date > datetime.date.today():
            raise ErreurDate('''La date ne peut être ultérieure à la date d'aujourd'hui''')
        titres = {}
        for date_achat, couple_titre in self.achats.items():  # Parcourir toutes les dates d'achat.
            if date_achat <= date:
                for symbole, quantite in couple_titre.items():  # Parcourir toutes les symboles
                    # achetés à cette date
                    if titres.get(symbole) is None:  # C'est la première achat de ce symbole
                        titres[symbole] = quantite
                    else:  # Ce symbole a déjà été acheté dans le passé
                        titres[symbole] += quantite
        for date_vente, couple_titre in self.ventes.items():  # Parcourir toutes les dates de vente.
            if date_vente <= date:
                for symbole, quantite in couple_titre.items():
                    titres[symbole] -= quantite
        return titres

    def vendre(self, symbole, quantite, date=datetime.date.today()):
        """Permet de vendre des titres"""
        if date > datetime.date.today():
            raise ErreurDate('''La date ne peut être ultérieure à la date d'aujourd'hui''')
        if self.titres(date)[symbole] < quantite:  # On ne possède pas les titres qu'on veut vendre.
            raise ErreurQuantité('Vous ne possédez pas les titres que vous voulez vendre')
        if self.ventes.get(date) is None:  # Il n'y a pas encore eu de vente à cette date
            self.ventes[date] = {symbole: quantite}
        elif self.ventes[date].get(symbole) is None:  # Il n'y a pas encore eu de vente
            # de ce titre à cette date
            self.ventes[date][symbole] = quantite
        else:  # Il y a déja eu vente de ce titre à cette date
            self.ventes[date][symbole] += quantite
        prix = quantite * self.marché.prix(symbole, date)
        self.déposer(prix, date)

    def valeur_totale(self, date=datetime.date.today()):
        """Permet de calculer la valeur totale du portefeuille (solde + titres)"""
        if date > datetime.date.today():
            raise ErreurDate('''La date ne peut être ultérieure à la date d'aujourd'hui''')
        valeur = self.solde(date)  # Solde présent dans le portefeuille à la date spécifiée
        for symbole in self.titres(date):  # Valeur de toutes les titres
            # possédés à la date spécifiée
            valeur += self.valeur_des_titres([symbole], date)
        return valeur

    def valeur_des_titres(self, symboles, date=datetime.date.today()):
        """Permet de calculer la valeur des titres"""
        if date > datetime.date.today():
            raise ErreurDate('''La date ne peut être ultérieure à la date d'aujourd'hui''')
        valeur = 0
        for symbole in symboles:
            valeur += self.titres(date).get(symbole, 0) * self.marché.prix(symbole, date)
        return valeur

    def valeur_projetée(self, date, rendement):
        """Permet de calculer la valeur projetée des titres"""
        if date <= datetime.date.today():
            raise ErreurDate('''La date ne peut être inférieure ou égale à la
             date d'aujourd'hui''')
        valeur = 0
        titres = self.titres()  # Titres possédés aujourd'hui
        jours = (date - datetime.date.today()).days
        if isinstance(rendement, float):  # Vérifie si le rendement est un nombre
            for symbole in titres:  # Parcourir toutes les titres possédés
                # à la date d'aujourd'hui
                valeur += self.valeur_des_titres([symbole])  # Valeur des titres aujourd'hui
            valeur = valeur*(1+rendement/100)**(jours//365)
            valeur += ((jours % 365)/365)*valeur*rendement/100
        else:  # Le rendement est un dictionnaire
            for symbole in titres:
                valeur_symbole = self.valeur_des_titres([symbole])
                valeur_symbole = valeur_symbole*(1+rendement.get(symbole, 0)/100)**(jours//365)
                valeur_symbole += ((jours % 365)/365)*valeur_symbole*rendement.get(symbole, 0)/100
                valeur += valeur_symbole
        return valeur
