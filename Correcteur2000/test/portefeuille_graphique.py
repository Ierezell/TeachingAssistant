"""Classe PortefeuilleGraphique (Dérivée de Portefeuille)"""
import datetime
import numpy
import matplotlib.pyplot as mpl
from portefeuille import Portefeuille


class PortefeuilleGraphique(Portefeuille):
    """Classe PortefeuilleGraphique - Classe Portefeuille + affichages graphiques"""
    def graph_solde(self, affichage):
        """Affiche l'historique des liquidités jusqu'à aujourd'hui"""
        if affichage:
            soldes = [0, 0]
            dates = []
            for date_dépot, montant in self.dépots.items():
                dates.append(date_dépot)
                soldes.append(soldes[-1] + sum(montant))
            mpl.plot(dates, soldes[2::], '-or')
            mpl.xlabel('Date')
            mpl.ylabel('Solde [$]')
            mpl.title('Historique des liquidités du portefeuille')
            mpl.grid(True)
            mpl.show()

    def graph_titres(self, affichage, titres):
        """Affiche l'historique des quantités d'actions pour les titres spécifiés"""
        if affichage:
            date = list(self.dépots.keys())[0]  # début
            date_fin = datetime.date.today()
            un_jour = datetime.timedelta(days=1)
            liste_titres = []
            dates = []
            while date <= date_fin:
                liste_titres.append(self.titres(date))
                dates.append(date)
                date += un_jour
            for symbole in titres:
                quantite = []
                for dictionnaire in liste_titres:
                    quantite.append(dictionnaire.get(symbole, 0))
                mpl.plot(dates, quantite)
            mpl.xlabel('Date')
            mpl.ylabel('Quantité')
            mpl.title("Historique des quantités d'action possédées")
            mpl.legend(list(titres))
            mpl.grid(True)
            mpl.show()

    def graph_valeur(self, affichage, titres):
        """Affiche l'historique de la valeur totale des titres spécifiés"""
        if affichage:
            for titre in titres:
                date = list(self.dépots.keys())[0]  # début
                date_fin = datetime.date.today()
                un_jour = datetime.timedelta(days=1)
                date_fin -= un_jour
                liste_valeur = []
                dates = []
                while date <= date_fin:
                    liste_valeur.append(self.valeur_des_titres(titre, date))
                    dates.append(date)
                    date += un_jour
                mpl.plot(dates, liste_valeur)
            mpl.xlabel('Date')
            mpl.ylabel('Valeur [$]')
            mpl.title("Historique de la valeur totale des titres")
            mpl.legend(list(titres))
            mpl.grid(True)
            mpl.show()

    def graph_projection(self, affichage, nb_prog, dico_rendements, dico_volatilités):
        """Affiche les quartiles de projections, aux 3 mois, sur 5 ans"""
        if affichage:
            date = datetime.date.today()
            ecart_3mois = datetime.timedelta(days=30)
            date += ecart_3mois
            dates = []
            q1 = []
            q2 = []
            q3 = []
            for _ in range(20):
                tbl_dico_rendements = {}  # Dictionnaire avec 10000 rendements par titre
                for titre, rendement in dico_rendements.items():
                    tbl_dico_rendements[titre] = numpy.random.normal(rendement,
                                                                     dico_volatilités[titre],
                                                                     nb_prog)
                tbl_valeurs_proj = numpy.zeros(nb_prog)
                for i in range(0, nb_prog):
                    print(i)
                    rendement = {}
                    for titre, tableau in tbl_dico_rendements.items():
                        rendement[titre] = tableau[i]
                    print(rendement)
                    tbl_valeurs_proj[i] = self.valeur_projetée(date, rendement)
                dates.append(date)
                q1.append(numpy.percentile(tbl_valeurs_proj, 25))
                q2.append(numpy.percentile(tbl_valeurs_proj, 50))
                q3.append(numpy.percentile(tbl_valeurs_proj, 75))
            mpl.plot(dates, q1, '-or')
            mpl.plot(dates, q2, '-ob')
            mpl.plot(dates, q3, '-og')
            mpl.xlabel('Date')
            mpl.ylabel('Valeur projetée [$]')
            mpl.title("Valeurs des titres projetée")
            mpl.legend('Q1', 'Q2', 'Q3')
            mpl.grid(True)
            mpl.show()
