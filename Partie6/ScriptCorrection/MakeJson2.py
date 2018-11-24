import sys
import re
import glob
import os
import json
reFichierNonTrouve = re.compile(r"La recherche", flags=re.MULTILINE)
reFonctionnement = re.compile(
    r"test_fonctionnement.+\.\.\.\s(.+)$\n", flags=re.MULTILINE)
reResults = re.compile(
    r"test_params.+\.\.\.\s((?:ok)|(?:FAIL)|(?:ERROR))$\n", flags=re.MULTILINE)
reCommentaires = re.compile(
    r"Ran 4 .+$\n\nFAILED.+$\n((?:.+\n\n?)*)", flags=re.MULTILINE)
reRapportErreur = re.compile(
    r"Ran 1 .+$\n\nFAILED.+$\n((?:.+\n\n?)*\n\n.+\n.+\n)", flags=re.MULTILINE)
filesDepth1 = glob.glob('../unbundled/*/Resultat_*.txt')
listJson = []
moyenne = 0
nb_corrige = 0
for filename in filesDepth1:
    GroupNb = filename[-7:-4]
    print(GroupNb)
    dicEquipe = {'équipe': GroupNb, 'score': 0, 'commentaires': ''}
    with open(filename) as file:
        content = file.read()
        plop = reFichierNonTrouve.findall(content)
    print("Fichier non : ", plop)
    if reFichierNonTrouve.match(content):
        dicEquipe['score'] = 0
        dicEquipe['commentaires'] = """<pre> Il n'y avait pas de fichier projet1.py dans le dossier de votre bundle </pre>"""
    else:
        fonctionne = reFonctionnement.findall(content)[0]
        commentaires = reCommentaires.findall(content)
        print("comment", commentaires)
        if fonctionne == 'ERROR':
            rapportErreur = reRapportErreur.findall(content)
            dicEquipe['score'] = 0
            dicEquipe['commentaires'] = """<h3> Votre programme n'a pas fonctionné durant la correction... </h3>"""
            if rapportErreur:
                dicEquipe['commentaires'] += """<pre> Un premier test (-v=volume -d=2018-09-21 -f=2018-09-24 goog) à été effectué mais votre programme à soulevé une erreur.\n{} </pre>""".format(
                    rapportErreur)
            else:
                dicEquipe['commentaires'] += """<pre> Un premier test (-v=volume -d=2018-09-21 -f=2018-09-24 goog) à été effectué mais votre programme à soulevé une erreur.</pre>"""

        else:
            if fonctionne == 'FAIL':
                dicEquipe['score'] = 40
            elif fonctionne == 'ok':
                dicEquipe['score'] = 60
            results = reResults.findall(content)
            print("results", results)
            bareme = {('ok', 0): 13, ('FAIL', 0): 10, ('ERROR', 0): 0,
                      ('ok', 1): 13, ('FAIL', 1): 8, ('ERROR', 1): 0,
                      ('ok', 2): 8,  ('FAIL', 2): 6, ('ERROR', 2): 0,
                      ('ok', 3): 6,  ('FAIL', 3): 4, ('ERROR', 3): 0}
            dicEquipe['score'] += sum([bareme[i, r]
                                       for r, i in enumerate(results)])
            if commentaires:
                dicEquipe['commentaires'] = "<pre>"
                for com in commentaires:
                    dicEquipe['commentaires'] += com + "\n"
                dicEquipe['commentaires'] += "</pre>"

    moyenne += dicEquipe['score']
    nb_corrige += 1
    listJson.append(dicEquipe)

pathJson = './ResultatsC3.json'
with open(pathJson, 'w+') as fileJson:
    json.dump(listJson, fileJson)
