import json
import re
import copy
import requests
from math import ceil
from subprocess import PIPE, Popen, TimeoutExpired
from time import sleep

"""
TODO: S'assurer que tous les de sauvegarde de l'équipe
      sont supprimé une fois le test terminé pour cette équipe.
TODO: Garder une copie du dictionnaire par équipe pour
      faciliter la révision de note.
TODO: Créer une nouvelle moulinette pour créer un JSON pour le téléversement.
      La moulinette séparé de préférence pour facilité la modularité dans le futur.
"""

# Modifier le nom utilisé par votre environnement pour python
# ex : py, python, python3.7, python3
PYENVNAME = "python3.7"

HEADER = '\033[95m'
OK = '\033[94m'
PASS = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def fillJson(pathJson: str, projetpath: str) -> dict:
    globalRes = 0
    with open(pathJson) as jsonFile:
        dictCritere = json.load(jsonFile)
    for critere in dictCritere:
        if critere["critere"] == "3":
            commandesToTest = critere["command"]
            reAttendu = [re.compile(resAtt, flags=re.MULTILINE)
                        for resAtt in critere["attendu"]]
            reErrAttendu = [re.compile(errAtt, flags=re.MULTILINE)
                            for errAtt in critere["erreurAttendu"]]
            print(f"{HEADER}    {critere['nom'][4:]}{ENDC}")
            for command in commandesToTest:
                """
                ma variable d'environnement est python3.7
                TODO: la changer pour toi
                """
                pyEnv = PYENVNAME
                options = [pyEnv, projetpath] + command[0].strip().split(" ")
                print(
                    f"      {options[1][-10:]} {BOLD}{WARNING}{' '.join(options[2:])}{ENDC}")
                result, err = [], []
                proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
                """
                Timeout augmenté à 10 car causait problème
                """
                timeout = False
                try:
                    result, err = proc.communicate(timeout=5)
                except TimeoutExpired:
                    timeout = True
                    print(f'{FAIL}        {command[0]} Time out{ENDC}')
                    critere["erreur"].append(
                        (f"""<li>{command[3]}</li>"""))
                critere["sortie"].append(f"RESULT : {result}")
                critere["sortie"].append(f"ERREUR : {err}")
                if command[1] == "PASS" and not timeout:
                    msg = reAttendu[command[2]].findall(result)
                    if reAttendu[command[2]].findall(result):
                        print(
                            f'{PASS}        {msg[0]}{ENDC}')
                    else:
                        print(
                            f'{FAIL}        {command[3]}{ENDC}')
                        critere["erreur"].append(
                            (f"""<li>{command[3]}</li>"""))
                elif command[1] == "FAIL" and not timeout:
                    msg = reErrAttendu[command[2]].findall(err)
                    if msg:
                        print(
                            f'{PASS}        {msg[0]}{ENDC}')
                    elif re.compile("pandas").findall(err):
                        print(
                            f'{FAIL}        Utilisation de pandas{ENDC}')
                        critere["erreur"].append(
                            (f"""<li>Utilisation d'une librairie non autorisée.</li>"""))
                    else:
                        print(f'{FAIL}        {command[3]}{ENDC}')
                        critere["erreur"].append(
                            (f"""<li>{command[3]}</li>"""))
            """
            Une pondération à été fait pour chaque critère
            La note est évalué selon la pondération
            La note est ensuite majoré à l'entier près supérieur (correction mode gentil)
            """
            note = (len(critere["command"]) - len(critere["erreur"])
                    ) / len(critere["command"]) * critere["ponderation"]
            if (critere["ponderation"]/2) <= int(ceil(note)) < critere["ponderation"]:
                print(
                    f'{BOLD}    Note : {ENDC}{WARNING}{int(ceil(note))}{ENDC}{BOLD}/{ENDC}{PASS}{critere["ponderation"]}\n{ENDC}')
            elif int(ceil(note)) < (critere["ponderation"]/2):
                print(
                    f'{BOLD}    Note : {ENDC}{FAIL}{int(ceil(note))}{ENDC}{BOLD}/{ENDC}{PASS}{critere["ponderation"]}\n{ENDC}')
            else:
                print(
                    f'{BOLD}    Note : {ENDC}{PASS}{int(ceil(note))}{ENDC}{BOLD}/{ENDC}{PASS}{critere["ponderation"]}\n{ENDC}')
            critere["note"] = int(ceil(note*.90))
            globalRes += int(ceil(note*.90))
    if 50 <= globalRes < 100:
        print(
            f'{BOLD}  Critère {critere["critere"]} : {ENDC}{WARNING}{globalRes}{ENDC}{BOLD}/{ENDC}{PASS}100{ENDC}')
    elif globalRes < 50:
        print(
            f'{BOLD}  Critère {critere["critere"]} : {ENDC}{FAIL}{globalRes}{ENDC}{BOLD}/{ENDC}{PASS}100{ENDC}')
    else:
        print(
            f'{BOLD}  Critère {critere["critere"]} : {ENDC}{PASS}{globalRes}{ENDC}{BOLD}/{ENDC}{PASS}100{ENDC}')
    return dictCritere
