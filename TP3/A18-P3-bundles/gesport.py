""".

Cette application sert à gérer un ou de plusieurs portefeuilles d'actions.

Ce script requiert que les modules `portefeuille`, `marche_boursier` et
`outils` développés dans le cadre du même projet.

Ce projet est conçu dans le cadre du cours GLO-1901.
Conçu par : Junior Cortentbach, Nguyễn Huy Dũng et René Chenard
Présenté à : Marc Parizeau

"""

import argparse
import numpy as np
from outils import Data, Date
from portefeuille import Portefeuille
import graphique


def commands_parser() -> argparse.Namespace:
    """.

    Fonction qui sert à extraire les commandes entrées au terminal.

    """
    parser = argparse.ArgumentParser(prog='ACTION',
                                     add_help=False)
    sub_parser = parser.add_subparsers(help="Choix de l'action")

    parser.add_argument('-d',
                        '--date',
                        metavar='DATE',
                        dest='date',
                        default='',
                        type=str,
                        help='Date effective (par défaut, date du jour)')
    parser.add_argument('-q',
                        '--quantité',
                        metavar='INT',
                        dest='quantité',
                        default=1,
                        type=int,
                        help='Quantité désirée (par défaut: 1)')
    parser.add_argument('-t',
                        '--titres',
                        metavar='STRING',
                        dest='titres',
                        default=[],
                        nargs='*',
                        type=str,
                        help='Le ou les titres à considérer (par défaut, tous'
                             ' les titres du portefeuille sont considérés)')
    parser.add_argument('-r',
                        '--rendement',
                        metavar='FLOAT',
                        dest='rendement',
                        default=0,
                        type=float,
                        help='Rendement annuel global (par défaut, 0)')
    parser.add_argument('-v',
                        '--volatilité',
                        metavar='FLOAT',
                        dest='volatilité',
                        default=0,
                        type=float,
                        help='Indice de volatilité global sur le rendement'
                             ' annuel (par défaut, 0)')
    parser.add_argument('-g',
                        '--graphique',
                        metavar='BOOL',
                        dest='graphique',
                        default=False,
                        type=bool,
                        help='Affichage graphique (par défaut, pas '
                             'd\'affichage graphique)')
    parser.add_argument('-p',
                        '--portefeuille',
                        metavar='STRING',
                        dest='portefeuille',
                        default='folio',
                        type=str,
                        help='Nom de portefeuille (par défaut, utiliser '
                             'folio)')

    déposer = sub_parser.add_parser('déposer', parents=[parser])
    acheter = sub_parser.add_parser('acheter', parents=[parser])
    vendre = sub_parser.add_parser('vendre', parents=[parser])
    solde = sub_parser.add_parser('solde', parents=[parser])
    titres = sub_parser.add_parser('titres', parents=[parser])
    valeur = sub_parser.add_parser('valeur', parents=[parser])
    projection = sub_parser.add_parser('projection', parents=[parser])

    parser.set_defaults(act=None, action=parser.print_help)
    déposer.set_defaults(act='déposer')
    acheter.set_defaults(act='acheter')
    vendre.set_defaults(act='vendre')
    solde.set_defaults(act='solde')
    titres.set_defaults(act='titres')
    valeur.set_defaults(act='valeur')
    projection.set_defaults(act='projection')

    return parser.parse_args()


class GesPort:
    """.

    Classe qui gère les fonctions principales de l'application.

    """
    def __init__(self, portefeuille: str) -> None:
        """.

        Initialise la classe GesPort en récupérant l'information entreposé dans
        un fichier JSON, s'il existe.

        """
        self.fichier = Data("{}.json".format(portefeuille), 'portefeuilles')

        self.nom = self.fichier.get_or_set('nom', portefeuille)

        actions = self.fichier.get_value('actions')
        fonds = self.fichier.get_value('fonds')
        journal = self.fichier.get_value('journal')

        load = {'actions': actions, 'fonds': fonds, 'journal': journal} if \
            any([actions, fonds, journal]) else None

        self.portefeuille = Portefeuille(load=load)
        self.fichier.get_or_set('actions', actions)
        self.fichier.get_or_set('fonds', fonds)
        self.fichier.get_or_set('journal', journal)

    def déposer(self, args: argparse.Namespace) -> None:
        """.

        Méthode servant à déposer la quantité de dollars spécifiée, à la date
        spécifiée.

        """
        réponse = self.portefeuille.déposer(args.quantité, Date.std(args.date))
        print(réponse)
        self.__update_values()

    def acheter(self, args: argparse.Namespace) -> None:
        """.

        Méthode servant à acheter la quantité spécifiée des titres spécifiés,
        à la date spécifiée.

        """
        for symbole in args.titres:
            réponse = self.portefeuille.acheter(
                symbole, args.quantité, Date.std(args.date))
            print(réponse)
        self.__update_values()

    def vendre(self, args: argparse.Namespace) -> None:
        """.

        Méthode servant à vendre la quantité spécifiée des titres spécifiés, à
        la date spécifiée.

        """
        for titre in args.titres:
            réponse = self.portefeuille.vendre(
                titre, args.quantité, Date.std(args.date))
            print(réponse)
        self.__update_values()

    def solde(self, args: argparse.Namespace) -> None:
        """.

        Méthode servant à afficher le solde en dollars des liquidités, à la
        date spécifiée.

        """
        print(self.portefeuille.solde(Date.std(args.date)))
        if args.graphique:
            graphique.PortefeuilleGraphique.tracer_solde(self.portefeuille)

    def titres(self, args: argparse.Namespace) -> None:
        """.

        Méthode servant à afficher les nombres d'actions détenues pour chacun
        des titres spécifiés, à la date spécifiée.

        """
        for titre, quantité in self.portefeuille.titres(
                Date.std(args.date)).items():
            print('{}={}'.format(titre, quantité))
        if args.graphique:
            graphique.PortefeuilleGraphique.tracer_titres(self.portefeuille)

    def valeur(self, args: argparse.Namespace) -> None:
        """.

        Méthode servant à afficher la valeur totale des titres
        spécifiés, à la date spécifiée.

        """
        print(round(self.portefeuille.valeur_des_titres(
            args.titres, Date.std(args.date)), 2))
        if args.graphique:
            graphique.PortefeuilleGraphique.tracer_valeur_totale(
                self.portefeuille)

    def projection(self, args: argparse.Namespace) -> None:
        """.

        Méthode servant à projeter la valeur totale des titres spécifiés, à
        la date future spécifiée, en tenant compte des rendements et indices de
        volatilité spécifiés.

        de la valeur à 2 décimales. Créer une description de la fonction.

        """
        titres = self.__titre_format(args.titres,
                                     args.rendement,
                                     args.volatilité)
        date = Date.std(args.date)
        nb_element = 10000
        liste_quartiles = []

        quartile1 = {}
        quartile2 = {}
        quartile3 = {}
        for titre in titres:
            liste_rendement = np.random.normal(float(titres[titre][0]),
                                               titres[titre][1], nb_element)
            quartile1[titre] = np.percentile(liste_rendement, 0.25)
            quartile2[titre] = np.percentile(liste_rendement, 0.50)
            quartile3[titre] = np.percentile(liste_rendement, 0.75)

            liste_quartiles.append(self.portefeuille.valeur_projetée(
                date=date,
                rendement=quartile1))
            liste_quartiles.append(self.portefeuille.valeur_projetée(
                date=date,
                rendement=quartile2))
            liste_quartiles.append(self.portefeuille.valeur_projetée(
                date=date,
                rendement=quartile3))
            print(liste_quartiles)
        if args.graphique:
            graphique.tracer_projection(liste_quartiles)

    def __update_values(self) -> None:
        """.

        Méthode privée servant à mettre à jours les informations du fichier.

        """
        self.fichier.update_value(
            'fonds', self.portefeuille.rapport('fonds'))
        self.fichier.update_value(
            'actions', self.portefeuille.rapport('actions'))
        self.fichier.update_value(
            'journal', self.portefeuille.rapport('journal'))

    @staticmethod
    def __titre_format(titres: list,
                       mu_defaut: float,
                       sigma_defaut: float) -> dict:
        """

        Méthode servant à formatter les titres venant avec un rendement et une
        volativité spécifiée.

        """
        dic = {}
        if titres:
            for titre in titres:
                if titre.find('(') != -1:
                    symbol = titre[:titre.find('(')]
                    mu_normal = float(
                        titre[titre.find('(') + 1:titre.find(',')])
                    sigma = float(titre[titre.find(',') + 1:titre.find(')')])
                    dic[symbol] = (mu_normal, sigma)
                else:
                    dic[titre] = (mu_defaut, sigma_defaut)
        return dic


def init() -> None:
    """.

    Fonction servant à initialiser l'application en fonction des commandes du
    terminal.

    """
    args = commands_parser()
    portefeuille = GesPort(args.portefeuille)
    actions = {
        "déposer": portefeuille.déposer,
        "acheter": portefeuille.acheter,
        "vendre": portefeuille.vendre,
        "solde": portefeuille.solde,
        "titres": portefeuille.titres,
        "valeur": portefeuille.valeur,
        "projection": portefeuille.projection
    }
    if args.act:
        actions[args.act](args)
    else:
        args.action()


# C'est ici que l'application s'initialise...
if __name__ == '__main__':
    init()
