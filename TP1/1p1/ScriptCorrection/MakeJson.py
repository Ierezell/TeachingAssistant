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
    r"(?<=Vous avez)(?:.+:\s\s(.+$\n))La bonne réponse était :$\n((?:.+\n){2})Votre réponse était :$\n(.+\n(?:[^V].+\n)?)\n?(?:Votre erreur est : \n((?:.+\n)*))?", flags=re.MULTILINE)
reRapportErreur = re.compile(
    r"(?<=Votre erreur est : \n)((?:.+\n)*)(?=(?:Vous)*)", flags=re.MULTILINE)
reNomTestFonctionnement = re.compile(
    r"fonctionnement :  (.+$\n)", flags=re.MULTILINE)
filesDepth1 = glob.glob('../unbundled/*/Resultat_*.txt')
listJson = []
moyenne = 0
nb_corrige = 0
for filename in filesDepth1:
    GroupNb = filename[-7:-4]
    print(GroupNb)
    dicEquipe = {'équipe': GroupNb, 'score': 0,
                 'commentaires': '<h3>Résultat critère 3</h3>'}
    with open(filename) as file:
        content = file.read()
        plop = reFichierNonTrouve.findall(content)
    if reFichierNonTrouve.match(content):
        dicEquipe['score'] = 0
        dicEquipe['commentaires'] += "<p>Il n'y a pas de fichier projet1.py dans le dossier de votre bundle.</p>"
    else:
        fonctionne = reFonctionnement.findall(content)[0]
        commentaires = reCommentaires.findall(content)
        nomTestFonc = reNomTestFonctionnement.findall(content)
        if nomTestFonc:
            nomTestFonc = nomTestFonc[0]
        if fonctionne == 'ERROR':
            rapportErreur = reRapportErreur.findall(content)
            dicEquipe['score'] = 0
            dicEquipe['commentaires'] += "<p>Votre programme n'a pas fonctionné durant la correction...</p>"
            print("rapport erreur", rapportErreur)
            if rapportErreur:
                dicEquipe['commentaires'] += """
<p>Un premier test (<code>{}</code>) a été effectué mais votre programme à soulevé une erreur.
Il y a peut-être une boucle infinie ou une erreur d'implémentation sur le fonctionnement basique.</p>
<p>Votre erreur : <p>
<pre>{}</pre>
""".format(nomTestFonc, rapportErreur[0])
            else:
                dicEquipe['commentaires'] += """
<p>Un premier test (<code>{}</code>) a été effectué mais votre programme à soulevé une erreur.</p>
Il y a peut-être une boucle infinie ou une erreur d'implémentation sur le fonctionnement basique.</p>
""".format(nomTestFonc)
        else:
            if fonctionne == 'FAIL':
                dicEquipe['score'] = 40
            elif fonctionne == 'ok':
                dicEquipe['score'] = 60
            results = reResults.findall(content)
            bareme = {('ok', 0): 15, ('FAIL', 0): 12, ('ERROR', 0): 0,
                      ('ok', 1): 15, ('FAIL', 1): 10, ('ERROR', 1): 0,
                      ('ok', 2): 10,  ('FAIL', 2): 8, ('ERROR', 2): 0}
            dicEquipe['score'] += sum([bareme[i, r]
                                       for r, i in enumerate(results)])

            if commentaires:
                for i in range(len(commentaires)):
                    print("Commentaires", len(commentaires))
                    print(commentaires[i][0])
                    print(commentaires[i][1])
                    print(commentaires[i][2])
                    print(commentaires[i][3])
                    if commentaires[i][0] == nomTestFonc:
                        dicEquipe['commentaires'] += """
<p>Vous avez échoué le test de fonctionnement : <CODE>{}</CODE></p>
<p>La bonne réponse est : </p>
<pre>{}</pre>
<p>Votre réponse est : </p>
<pre>{}</pre>""".format(commentaires[i][0], commentaires[i][1], commentaires[i][2])
                        if commentaires[i][3]:
                            dicEquipe['commentaires'] += """<p>Votre erreur est : </p>
<pre>{}</pre>""".format(commentaires[i][3])
                    else:
                        dicEquipe['commentaires'] += """
<p>Vous avez échoué le test : <CODE>{}</CODE></p>
<p>La bonne réponse est : </p>
<pre>{}</pre>
<p>Votre réponse est : </p>
<pre>{}</pre>""".format(commentaires[i][0], commentaires[i][1], commentaires[i][2])
                        if commentaires[i][3]:
                            dicEquipe['commentaires'] += """<p>Votre erreur est : </p>
<pre>{}</pre>""".format(commentaires[i][3])
            else:
                dicEquipe['commentaires'] += """<p>Bravo, vous avez passé tout les tests.</p>"""
    dicEquipe['commentaires'] = dicEquipe['commentaires'].replace('\\n', '\n')
    moyenne += dicEquipe['score']
    nb_corrige += 1
    listJson.append(dicEquipe)
print("MOYENNE", moyenne/nb_corrige)
pathJson = './ResultatsC3_'+GroupNb+'.json'
with open(pathJson, 'w+') as fileJson:
    json.dump(listJson, fileJson)
