import glob
import json
import os
import shutil

from fillJsonTemplate import fillJson

# TP à corriger
TP = 'TP1'

# Nom du fichier principale du projet à tester
PROJECTNAME = "projet1.py"

# Modifier le numéro du critère au besoin
NOCRITERE = 1

if not os.path.exists(f"./{TP}/Resultats"):
    os.makedirs(f"./{TP}/Resultats")

bundlesEleves = glob.glob(f'./{TP}/unbundled/*')
filesCorrection = glob.glob(f'./{TP}/*')
print(f"Nombre de bundles au total : {len(bundlesEleves)}")
ResultSiteWeb = []
correctfile = 0

for bundle in bundlesEleves:
    filesAvecPortefeuilleEleve = glob.glob(f'./{TP}/*')

    # Retire les fichiers de sauvegarde des étudiants (TP3)
    for files in filesAvecPortefeuilleEleve:
        if files not in filesCorrection:
            try:
                os.remove(files)
            except IsADirectoryError:
                shutil.rmtree(files)

    GroupNb = bundle[-9:-6]
    subdir = bundle[-16:]
    sous_repertoire = glob.glob(f"./{TP}/unbundled/{subdir}/*")
    noProject = True
    listFilesFound = []

    for subdirname in sous_repertoire:
        filename = subdirname[30:]
        listFilesFound.append(filename)

        if filename == PROJECTNAME:
            correctfile += 1
            noProject = False
            pathcall = os.path.join(".", TP, "unbundled", subdir, PROJECTNAME)
            dictDetail = fillJson(f'./{TP}/dictCritere.json', pathcall)
            pathSaveEleve = f"./{TP}/Resultats/Resultat_{GroupNb}.json"
            with open(pathSaveEleve, 'w') as outfile:
                json.dump(dictDetail, outfile, ensure_ascii=False)

# TODO : transformer ça en méthode pour AssistantCorrection
    # if noProject:
    #     critereJSON = f'<h4>Résultat critère {NOCRITERE}</h4>'
    #     dicEquipeCritereFail = {'équipe': GroupNb, 'score': 0,
    #                             'commentaires': critereJSON}
    #     dicEquipeCritereFail['commentaires'] += (
    #         f"<p>Il n'y a pas de fichier {PROJECTNAME}"
    #         f"dans le dossier de votre bundle.</p>"
    #         f"<p>Les seuls fichiers trouvés sont :</p>"
    #         f"<p>{listFilesFound}</p>")
    #     ResultSiteWeb.append(dicEquipeCritereFail)
    #     print(f"Aucun fichier {PROJECTNAME} pour le groupe : {GroupNb}")
    #     with open(f'./{TP}/ResultatsSiteWeb.json', 'w') as outfile:
    #         json.dump(ResultSiteWeb, outfile, ensure_ascii=False)
