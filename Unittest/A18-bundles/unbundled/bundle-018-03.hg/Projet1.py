import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-d", dest='DATE', help="debut de la date")
parser.add_argument("-f", dest='DATE', help="fin de la date")
parser.add_argument("-v", dest='{fermeture,ouverture,min,max,volume}', help="valeur boursiere")
parser.add_argument("symbole", help="Nom du symbole boursiere")
args = parser.parse_args

