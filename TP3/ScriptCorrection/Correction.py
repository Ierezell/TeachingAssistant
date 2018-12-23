import glob
import json
import os
import shutil

from fillJsonTemplate import fillJson

bundlesEleves = glob.glob('../unbundled/*')
filesCorrection = glob.glob('./*')
print(f"""Nombre de bundles au total : {len(bundlesEleves)}""")
with open('./dictCritere.json') as templateJson:
    criteres = sorted(list(set([d['critere'] for d in dictResultEleve])))

ResultSiteWeb = {}
for c in criteres:
    ResultSiteWeb[c] = []

correctfile = 0
for bundle in bundlesEleves:
    filesAvecPortefeuilleEleve = glob.glob('./*')
    for files in filesAvecPortefeuilleEleve:
        if files not in filesCorrection:
            try:
                os.remove(files)
            except IsADirectoryError:
                shutil.rmtree(files)
    GroupNb = bundle[-9:-6]
    subdir = bundle[-16:]
    sous_repertoire = glob.glob(f"../unbundled/{subdir}/*")
    noGesport = True
    listFilesFound = []
    for subdirname in sous_repertoire:
        filename = subdirname[30:]
        listFilesFound.append(filename)
        if filename == "gesport.py":
            correctfile += 1
            noGesport = False
            dictDetail = fillJson('./dictCritere.json', subdirname)
            pathSaveEleve = f"./Resultats/Resultat_{GroupNb}.json"
            with open(pathSaveEleve, 'w') as outfile:
                json.dump(dictDetail, outfile)

    if noGesport:
        dicEquipeCritereFail = {'équipe': GroupNb, 'score': 0,
                                'commentaires': '<h4>Résultat critère 1</h4>'}
        dicEquipeCritereFail['commentaires'] += (
            f"""<p>Il n'y a pas de fichier gesport.py dans le dossier de votre bundle.</p>"""
            f"""<p>Les seuls fichiers trouvés sont :</p>"""
            f"""<p>{listFilesFound}</p>""")
        for c in criteres:
            ResultSiteWeb[c].append(dicEquipeCritereFail)
        print(f"Aucun fichier gesport.py pour le groupe : {GroupNb}")
        with open('./ResultatsSiteWeb.json', 'w') as outfile:
            json.dump(ResultSiteWeb, outfile)
