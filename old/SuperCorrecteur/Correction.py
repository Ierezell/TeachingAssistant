import glob
import json
import os
import shutil

from fillJsonTemplate import fillJson

HEADER = '\033[95m'
OK = '\033[94m'
PASS = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# Nom du fichier principale du projet à tester
PROJECTNAME = "projet1.py" 

# Modifier le numéro du critère au besoin
NOCRITERE = 1

if not os.path.exists("./Resultats"):
    os.makedirs("./Resultats")
    
bundlesEleves = glob.glob('../unbundled/*')
filesCorrection = glob.glob('./*')
print(f"""Nombre de bundles au total : {PASS}{len(bundlesEleves)}{ENDC}""")
listFail = {}
ResultSiteWeb = []
correctfile = 0
for bundle in bundlesEleves:
    GroupNb = bundle[-9:-6]
    if int(GroupNb) == 23:
        filesAvecPortefeuilleEleve = glob.glob('./*')

        # Retire les fichiers de sauvegarde des étudiants (TP3)
        for files in filesAvecPortefeuilleEleve:
            if files not in filesCorrection:
                try:
                    os.remove(files)
                except IsADirectoryError:
                    shutil.rmtree(files)
        subdir = bundle[-16:]
        sous_repertoire = glob.glob(f"../unbundled/{subdir}/*")
        noProject = True
        listFilesFound = []
        print(
            f'\n{UNDERLINE}¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯{ENDC}\n')
        print(f'{BOLD}  ÉQUIPE {int(GroupNb)}{ENDC}\n')
        # print(f'\n  Fichier trouvé :')
        for subdirname in sous_repertoire:
            filename = subdirname[30:]
            listFilesFound.append(filename)
            # if noProject:
                # print(f'    - {filename}')
            if filename == PROJECTNAME:
                # print(f'\n  Début de la correction :')
                correctfile += 1
                noProject = False
                pathcall = os.path.join("..", "unbundled", subdir, PROJECTNAME)
                dictDetail = fillJson('dictCritere.json', pathcall)
                pathSaveEleve = f"./Resultats/Resultat_{GroupNb}.json"
                with open(pathSaveEleve, 'w') as outfile:
                    json.dump(dictDetail, outfile, ensure_ascii=False)

        if noProject:
            critereJSON = f'<h4>Résultat critère {NOCRITERE}</h4>'
            dicEquipeCritereFail = {'équipe': GroupNb, 'score': 0,
                                    'commentaires': critereJSON}
            dicEquipeCritereFail['commentaires'] += (
                f"""<p>Il n'y a pas de fichier {PROJECTNAME} dans le dossier de votre bundle.</p>"""
                f"""<p>Les seuls fichiers trouvés sont :</p>"""
                f"""<p>{listFilesFound}</p>""")
            ResultSiteWeb.append(dicEquipeCritereFail)
            msg = f"\nAucun fichier {PROJECTNAME} pour le groupe : {GroupNb}"
            listFail[msg] = listFilesFound
            print(f'{FAIL}  {msg}{ENDC}')
            with open('./ResultatsSiteWeb.json', 'w') as outfile:
                json.dump(ResultSiteWeb, outfile, ensure_ascii=False)

for msg, files in listFail.items():
    print(f'{HEADER}  {msg}{ENDC}')
    for file in files:
        print(f"{OK}    -{file}{ENDC}")
    print("\n")
