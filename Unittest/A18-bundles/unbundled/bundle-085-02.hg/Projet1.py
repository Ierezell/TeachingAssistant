import argparse
parser = argparse.ArgumentParser()
parser.add_argument("symbole", help="Nom du symbole boursier désiré")
parser.add_argument('-d', dest='DATE', default='{}', help="date d'ouverture")
parser.add_argument('-f', dest='DATE', default='{}', help="date de fermeture")
parser.add_argument('-v', dest='{fermeture, ouverture, min, max, volume}', default='{}', help="Valeur boursiere")
args = parser.parse_args()
