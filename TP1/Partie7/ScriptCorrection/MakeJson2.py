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
    r"(?<=Vous avez)(?:.+:\s\s(.+$\n))((?:.+$\n)*)", flags=re.MULTILINE)
reRapportErreur = re.compile(
    r"Ran 1 .+$\n\nFAILED.+$\n((?:.+\n\n?)*\n\n.+\n.+\n)", flags=re.MULTILINE)
filesDepth1 = glob.glob('../unbundled/*/Resultat_*.txt')
listJson = []
moyenne = 0
nb_corrige = 0
for filename in filesDepth1:
    GroupNb = filename[-7:-4]
    dicEquipe = {'équipe': GroupNb, 'score': 0,
                 'commentaires': '<h3>Résultat critère 3</h3>'}
    with open(filename) as file:
        content = file.read()
        plop = reFichierNonTrouve.findall(content)
    if reFichierNonTrouve.match(content):
        dicEquipe['score'] = 0
        dicEquipe['commentaires'] += "<p>Il n'y avait pas de fichier projet1.py dans le dossier de votre bundle</p>"
    else:
        fonctionne = reFonctionnement.findall(content)[0]
        commentaires = reCommentaires.findall(content)
        if fonctionne == 'ERROR':
            rapportErreur = reRapportErreur.findall(content)
            dicEquipe['score'] = 0
            dicEquipe['commentaires'] += "<p>Votre programme n'a pas fonctionné durant la correction...</p>"
            if rapportErreur:
                dicEquipe['commentaires'] += "<p>Un premier test (-v=volume -d=2018-09-21 -f=2018-09-24 goog) à été effectué mais votre programme à soulevé une erreur.\n{}</p>".format(
                    rapportErreur[0])
            else:
                dicEquipe['commentaires'] += "<p>Un premier test (-v=volume -d=2018-09-21 -f=2018-09-24 goog) à été effectué mais votre programme à soulevé une erreur.</p>"

        else:
            if fonctionne == 'FAIL':
                dicEquipe['score'] = 40
            elif fonctionne == 'ok':
                dicEquipe['score'] = 60
            results = reResults.findall(content)
            bareme = {('ok', 0): 13, ('FAIL', 0): 10, ('ERROR', 0): 0,
                      ('ok', 1): 13, ('FAIL', 1): 8, ('ERROR', 1): 0,
                      ('ok', 2): 8,  ('FAIL', 2): 6, ('ERROR', 2): 0,
                      ('ok', 3): 6,  ('FAIL', 3): 4, ('ERROR', 3): 0}
            dicEquipe['score'] += sum([bareme[i, r]
                                       for r, i in enumerate(results)])
            if commentaires:
                for i in range(len(commentaires)):
                    dicEquipe['commentaires'] += "<p>Vous avez échoué le test : <CODE>{}</CODE></p><pre>{}</pre>".format(
                        commentaires[i][0], commentaires[i][1])
    dicEquipe['commentaires'] = dicEquipe['commentaires'].replace('\\n', '\n')
    moyenne += dicEquipe['score']
    nb_corrige += 1
    listJson.append(dicEquipe)

pathJson = './ResultatsC3.json'
with open(pathJson, 'w+') as fileJson:
    json.dump(listJson, fileJson)
