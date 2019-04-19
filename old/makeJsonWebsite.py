import glob
import json
import os

# TP à corriger
TP = 'TP1'

# Choisir le critère à compiler pour le site en modifiant la valeur
NOCRITERE = 1

if not os.path.exists(f"./{TP}/Resultats/ResultatsCompiles"):
    os.makedirs(f"./{TP}/Resultats/ResultatsCompiles")

folderJsonDetail = glob.glob(f"./{TP}/Resultats/*.json")
Resultat = []
for pathJsonEleve in folderJsonDetail:
    groupNb = pathJsonEleve[-8:-5]
    print(groupNb)
    with open(pathJsonEleve) as infile:
        jsonEleve = json.load(infile)

    dictResult = {"équipe": groupNb,
                  'score': 0, 'commentaires': []}

    note = 0
    for test in jsonEleve:
        if test['critere'] == str(NOCRITERE):

            note += test["note"]
            if test["description"][-13:] != '</strong></p>':
                test["description"] = test["description"].replace(
                    '</p>', '</strong></p>')
            dictResult["commentaires"].append(f'{test["nom"]}: ')
            dictResult["commentaires"].append(
                f'[{test["note"]}/{test["ponderation"]}]')
            dictResult["commentaires"].append('</h3></p>')
            dictResult["commentaires"].append(
                f'{test["description"]}')
            if test["erreur"]:
                dictResult["commentaires"].append(f'{test["commentaire"]}')
                dictResult["commentaires"].append('<ul>')
                for err in test["erreur"]:
                    dictResult["commentaires"].append('<li>%s</li>' % err.replace('\n', '<br>'))
                    # dictResult["commentaires"].append(f'<li>{err}</li>')
                dictResult["commentaires"].append('</ul>')
    dictResult["commentaires"] = str.join('', dictResult["commentaires"])
    dictResult["commentaires"] = f"<p><h2>Évaluation du critère {str(NOCRITERE)} [{note}/100]</h2></p>" + \
        dictResult["commentaires"]
    print(dictResult["commentaires"])
    dictResult['score'] = note
    Resultat.append(dictResult)
with open(f'./{TP}/Resultats/ResultatsCompiles/ResultatCritere_{str(NOCRITERE)}.json', 'w') as outfile:
    json.dump(Resultat, outfile, ensure_ascii=False)


# "<p><h2>Évaluation du critère 1 [96/100]</h2></p>",
# "<p><h3>Commande Help : [60/60]</h3></p>",
# "<p><strong>V�rifier l'existence de la commande <code>help</code>.</strong></p>",
# "<p><h3>Nomenclature : [8/10]</h3></p>",
# "<p><strong>V�rifer la nomenclature des arguments et actions.</strong></p>",
# "<p>Des actions et/ou arguments sont mal nomm�s.</p>",
#  "<ul>",
# "<li><code>portefeuille</code> manquant donc mal nomm�e.</li>",
#  "</ul>",
# "<p><h3>Arguments superflus : [10/10]</h3></p>",
# "<p><strong>V�rifier que les actions n'ont pas d'arguments superflus.</strong></p>",
# "<p><h3>Arguments manquants : [8/10]</h3></p>",
# "<p><strong>V�rifier que les actions n'ont pas d'arguments manquants.</strong></p>",
# "<p>Des actions ont des arguments manquants.</p>",
#  "<ul>",
# "<li><code>argument <code>--portefeuille</code> manquant.</li>",
# "</ul><p><h3>Metavar : [10/10]</h3></p>",
# "<p><strong>V�rifier que les arguments ont le bon metavar.</strong></p>"
