"""
    Ce fichier contient la class qui traite l'affichage des graphiques
"""
import datetime
import matplotlib.pyplot as mpl
import portefeuille


class PortefeuilleGraphique(portefeuille.Portefeuille):
    """
        La class traitant l'affichage des graphiques
    """

    def tracer_solde(self):
        """
            La fonction traitant l'affichage le graphique solde.
        """
        ensemble = sorted(self.rapport('fonds'))
        date_min, date_max = portefeuille.Date.std(
            ensemble[0]), portefeuille.Date.std(ensemble[-1])
        date_abscisse = liste_date_abscisse(date_min, date_max)
        solde = []

        for i in date_abscisse:
            solde.append(self.solde(i))

        mpl.plot(solde, 'b')
        mpl.ylabel('Solde du portefeuille')
        mpl.legend(['solde'])
        mpl.title("L'historique des liquidités du portefeuille")

        decorer(date_abscisse)

    def tracer_titres(self):
        """
            La fonction traitant l'affichage le graphique titres.
        """
        date_min = datetime.date.today()
        date_max = datetime.date.today() + datetime.timedelta(-9999)
        for sym in self.rapport('actions'):
            date_min = min(date_min,
                           *(portefeuille.Date.std(i) for i in self.rapport(
                               'actions')[sym]))
            date_max = max(date_max,
                           *(portefeuille.Date.std(i) for i in self.rapport(
                               'actions')[sym]))
        date_abscisse = liste_date_abscisse(date_min, date_max)
        titres, legend = {}, []

        for sym in self.rapport('actions'):
            titres[sym] = []
            for i in date_abscisse:
                titres[sym].append(self.titres(i)[sym])
            mpl.plot(titres[sym])
            legend.append(sym)
        mpl.ylabel('Titres du portefeuille')
        mpl.legend(legend)
        mpl.title("L'historique des titres du portefeuille")

        decorer(date_abscisse)

    def tracer_valeur_totale(self):
        """
            La fonction traitant l'affichage le graphique valeur totale.
        """
        date_min = datetime.date.today()
        date_max = datetime.date.today() + datetime.timedelta(-9999)
        for sym in self.rapport('actions'):
            date_min = min(date_min,
                           *(portefeuille.Date.std(i) for i in self.rapport(
                               'actions')[sym]))
            date_max = max(date_max,
                           *(portefeuille.Date.std(i) for i in self.rapport(
                               'actions')[sym]))
        date_abscisse = liste_date_abscisse(date_min, date_max)
        valeur_totale = []

        for i in date_abscisse:
            valeur_totale.append(self.valeur_des_titres(date=i))

        mpl.plot(valeur_totale, 'b')
        mpl.ylabel('Valeur totale des titres du portefeuille')
        mpl.legend(['Valeur des titres'])
        mpl.title("L'historique de la valeur totale des titres du "
                  "portefeuille")

        decorer(date_abscisse)

def tracer_projection(liste_quartiles):
    """
        La fonction traitant l'affichage le graphique projection.
    """
    date_min = datetime.date.today()
    date_max = list(liste_quartiles[0].keys())[-1]
    date_abscisse = liste_date_abscisse(date_min, date_max)
    q_1, q_2, q_3 = [], [], []
    for date in date_abscisse:
        if liste_quartiles[0].get(date):
            q_1.append(liste_quartiles[0][date])
            q_2.append(liste_quartiles[1][date])
            q_3.append(liste_quartiles[2][date])
        else:
            q_1.append(q_1[-1])
            q_2.append(q_2[-1])
            q_3.append(q_3[-1])

    mpl.plot(q_1, 'y', q_2, 'b', q_3, 'r')
    mpl.ylabel('Valeur projetée')
    mpl.legend(['Q1', 'Q2', 'Q3'])
    mpl.title("Valeurs de projection")

    decorer(date_abscisse)


def liste_date_abscisse(date_min, date_max):
    """
        La fonction permettant de générer une liste des dates entre 2 dates
        spécifiées.
    """
    liste = []
    i = 0
    while date_min + datetime.timedelta(i) <= date_max:
        liste.append(date_min + datetime.timedelta(i))
        i += 1
    return liste


def decorer(date_tracer: list):
    """
        La fonction traitant le style des graphiques.
    """
    nbdate = len(date_tracer)
    mpl.xlabel('Date')
    mpl.xticks(range(0, nbdate, 1 + nbdate // 10),
               date_tracer[::1 + nbdate // 10],
               rotation=30)
    mpl.grid(True, linestyle='--')
    mpl.xlim([0, nbdate - 1])
    mpl.gcf().set_size_inches(10, 8)
    mpl.show()
