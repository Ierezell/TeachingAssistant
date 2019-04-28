"""Gestion de portefeuille"""
import argparse
import datetime
import pickle
import numpy
from portefeuille_graphique import PortefeuilleGraphique
from marche_boursier import MarchéBoursier

# PARSER principal
PARSER = argparse.ArgumentParser(description="Gestionnaire de portefeuille d'actions")

SUBPARSERS = PARSER.add_subparsers(title='ACTIONS', dest='ACTION')
PARSER_DEPOSER = SUBPARSERS.add_parser('déposer', help='Déposer la quantité de dollars spécifiée, '
                                                       'à la date spécifiée')
PARSER_ACHETER = SUBPARSERS.add_parser('acheter', help='Acheter la quantité spécifiée '
                                                       'des titres spécifiés, à la date spécifiée')
PARSER_VENDRE = SUBPARSERS.add_parser('vendre', help=' Vendre la quantité spécifiée des titres '
                                                     'spécifiés, à la date spécifiée')
PARSER_SOLDE = SUBPARSERS.add_parser('solde', help='Afficher en dollars le solde des liquidités, '
                                                   'à la date spécifiée')
PARSER_TITRES = SUBPARSERS.add_parser('titres', help="Afficher les nombres d'actions détenues"
                                                     " pour chacun des titres spécifiés, à la date "
                                                     "spécifiée; affichez une ligne"
                                                     " par titre, avec "
                                                     "le format titre=quantité")
PARSER_VALEUR = SUBPARSERS.add_parser('valeur', help="Afficher la valeur totale"
                                                     " des titres spécifiés,"
                                                     " à la date spécifiée;"
                                                     " affichez la valeur"
                                                     " sur une ligne,"
                                                     " en limitant l'affichage à 2 décimales")
PARSER_PROJECTION = SUBPARSERS.add_parser('projection', help="Projeter la valeur totale des"
                                                             " titres spécifiés,"
                                                             " à la date future spécifiée,"
                                                             " en tenant compte des"
                                                             " rendements et indices de"
                                                             " volatilité spécifiés; "
                                                             "affichez la projection"
                                                             " sur une seule ligne, "
                                                             "en limitant l'affichage de la valeur"
                                                             " à 2 décimales")

LISTE_SUBPARSERS = [PARSER_DEPOSER, PARSER_ACHETER, PARSER_VENDRE,
                    PARSER_SOLDE, PARSER_TITRES, PARSER_VALEUR, PARSER_PROJECTION]
for subparser in LISTE_SUBPARSERS:
    subparser.add_argument('-d', '--date', metavar='DATE', default=datetime.date.today(),
                           help='Date effective (par défaut, date du jour)')
    subparser.add_argument('-q', '--quantité', type=int, default=1, metavar='INT',
                           help='Quantité désirée (par défaut: 1)')
    subparser.add_argument('-t', '--titres', default='tous les titres', metavar='STRING', nargs='+',
                           help='Le ou les titres à considérer (par défaut, tous les titres du '
                                'portefeuille sont considérés)')
    subparser.add_argument('-r', '--rendement', metavar='FLOAT', type=float, default=0.0,
                           help='Rendement annuel global (par défaut, 0)')
    subparser.add_argument('-v', '--volatilité', metavar='FLOAT', type=float, default=0.0,
                           help='Indice de volatilité global sur le'
                                ' rendement annuel (par défaut, 0)')
    subparser.add_argument('-g', '--graphique', metavar='BOOL', type=bool, default=False,
                           help="Affichage graphique (par défaut, pas d'affichage graphique)")
    subparser.add_argument('-p', '--portefeuille', metavar='STRING', type=str, default='folio',
                           help='Nom de portefeuille (par défaut, utiliser folio)')

ARGUMENTS = PARSER.parse_args()

# Formattage de la date
if ARGUMENTS.date != datetime.date.today():
    ARGUMENTS.date = datetime.datetime.strptime(ARGUMENTS.date, '%Y-%m-%d').date()

# Ouverture du portefeuille demandé ou création d'un nouveau portefeuille si inexistant
try:
    FILE = open('{}.pkl'.format(ARGUMENTS.portefeuille), 'rb')
    u = pickle.Unpickler(FILE)
    PF = u.load()
    FILE.close()
except FileNotFoundError:
    PF = PortefeuilleGraphique(MarchéBoursier())

# Détermination des titres si valeur par défaut sélectionnée
if ARGUMENTS.titres == 'tous les titres':
    TITRES_PF = PF.titres(ARGUMENTS.date)
    ARGUMENTS.titres = TITRES_PF.keys()

# Détermination des rendements et volatilité
DICO_RENDEMENTS = {}
DICO_VOLATILITÉS = {}
NB_PROG = 10000
for titre in ARGUMENTS.titres:
    if titre[-1] == ')':  # Le titre est sous forme titre(rendement, volatilité)
        tuple_rend_vol = titre[4::]
        symbole = titre[0:4]
        tuple_rend_vol = eval(tuple_rend_vol)
        DICO_RENDEMENTS[symbole] = tuple_rend_vol[0]
        DICO_VOLATILITÉS[symbole] = tuple_rend_vol[1]
    else:
        DICO_RENDEMENTS[titre] = ARGUMENTS.rendement
        DICO_VOLATILITÉS[titre] = ARGUMENTS.volatilité

# Actions
if ARGUMENTS.ACTION == 'déposer':
    PF.déposer(ARGUMENTS.quantité, ARGUMENTS.date)

elif ARGUMENTS.ACTION == 'acheter':
    for titre in ARGUMENTS.titres:
        PF.acheter(titre, ARGUMENTS.quantité, ARGUMENTS.date)

elif ARGUMENTS.ACTION == 'vendre':
    for titre in ARGUMENTS.titres:
        PF.vendre(titre, ARGUMENTS.quantité, ARGUMENTS.date)

elif ARGUMENTS.ACTION == 'solde':
    SOLDE = PF.solde(ARGUMENTS.date)
    print('{:.2f} $'.format(SOLDE))
    PF.graph_solde(ARGUMENTS.graphique)

elif ARGUMENTS.ACTION == 'titres':
    TITRES_PF = PF.titres(ARGUMENTS.date)
    TITRES_DEMANDE = ARGUMENTS.titres
    for titre_PF, qte_titre in TITRES_PF.items():
        for titre_demande in TITRES_DEMANDE:
            if titre_PF == titre_demande:
                print('{} = {}'.format(titre_PF, qte_titre))
    PF.graph_titres(ARGUMENTS.graphique, ARGUMENTS.titres)

elif ARGUMENTS.ACTION == 'valeur':
    VALEUR = PF.valeur_des_titres(ARGUMENTS.titres, ARGUMENTS.date)
    print('{:.2f} $'.format(VALEUR))
    PF.graph_valeur(ARGUMENTS.graphique, ARGUMENTS.titres)

elif ARGUMENTS.ACTION == 'projection':
    TBL_DICO_RENDEMENTS = {}  # Dictionnaire avec 10000 rendements par titre
    for titre, rendement in DICO_RENDEMENTS.items():
        TBL_DICO_RENDEMENTS[titre] = numpy.random.normal(rendement, DICO_VOLATILITÉS[titre],
                                                         NB_PROG)
    TBL_VALEURS_PROJ = numpy.zeros(NB_PROG)
    for i in range(0, NB_PROG):
        print(i)
        rendement = {}
        for titre, tableau in TBL_DICO_RENDEMENTS.items():
            rendement[titre] = tableau[i]
        print(rendement)
        TBL_VALEURS_PROJ[i] = PF.valeur_projetée(ARGUMENTS.date, rendement)
    Q1 = numpy.percentile(TBL_VALEURS_PROJ, 25)
    Q2 = numpy.percentile(TBL_VALEURS_PROJ, 50)
    Q3 = numpy.percentile(TBL_VALEURS_PROJ, 75)
    print((Q1, Q2, Q3))
    PF.graph_projection(ARGUMENTS.graphique, NB_PROG, DICO_RENDEMENTS, DICO_VOLATILITÉS)

# Enregistrement du portefeuille
FILE = open('{}.pkl'.format(ARGUMENTS.portefeuille), 'wb')
p = pickle.Pickler(FILE)
p.dump(PF)
FILE.close()
