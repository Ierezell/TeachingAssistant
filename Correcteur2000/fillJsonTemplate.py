import json
import re
import copy
import requests
from math import ceil
from subprocess import PIPE, Popen
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
        commandesToTest = critere["command"]
        reAttendu = [re.compile(resAtt, flags=re.MULTILINE)
                     for resAtt in critere["attendu"]]
        reErrAttendu = [re.compile(errAtt, flags=re.MULTILINE)
                        for errAtt in critere["erreurAttendu"]]
        print(f"{HEADER}    {critere['nom'][4:]}{ENDC}")
        for args in commandesToTest:
            """
            ma variable d'environnement est python3.7
            TODO: la changer pour toi
            """
            pyEnv = PYENVNAME
            options = [pyEnv, projetpath] + args.strip().split(" ")
            print(f'      {options[1][-10:]} {BOLD}{WARNING}{options[2]}{ENDC}')
            result, err = [], []
            proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
            """
            Timeout augmenté à 10 car causait problème
            """
            result, err = proc.communicate(timeout=10)
            critere["sortie"].append(f"RESULT : {result}")
            critere["sortie"].append(f"ERREUR : {err}")
            if critere["critere"] == "1":
                testEchoue = True
                errFail = False

                if err:
                    reTempErrAtt = copy.deepcopy(reErrAttendu)
                    for index, regArg in enumerate(reErrAttendu):
                        if regArg.findall(err):
                            print(f'{PASS}        {regArg.findall(err)[0]}{ENDC}')
                            del reErrAttendu[index]
                            testEchoue = False
                            break
                        else:
                            print(f'{FAIL}        {reErrAttendu[index].pattern}{ENDC}')
                    if testEchoue:
                        errFail = True

                if result and testEchoue:
                    reTempAtt = copy.deepcopy(reAttendu)
                    for index, regArg in enumerate(reAttendu):
                        if regArg.findall(result):
                            """
                            Il y a un seul résultat attendu pour chaque commande testé
                            Si le résultat pour une commande est trouvé nous le modifions
                            de la liste au cas ou il puisse apparaître en double et nous
                            marquons le test comme non échoué.
                            """
                            print(
                                f'{PASS}        {regArg.findall(result)[0]}{ENDC}')
                            del reAttendu[index]
                            testEchoue = False
                            break
                        else:
                            print(f'{FAIL}        {reAttendu[index].pattern}{ENDC}')
                    if testEchoue and reAttendu != []:
                        critere["erreur"].append(
                            ("""<li><p>Dans le contexte suivant :</p>"""
                             f"""<p>"""
                             f"""<code>python3 {options[1][-10]} {options[2]}</code></p>"""
                             """<p>Votre code ne soulève pas d'erreur """
                             """mais ceci n'était pas le résultat attendu :<p>"""
                             f"""<pre class="language-python">"""
                             f"""<code>{result}</code></pre></li>"""))
                if testEchoue and errFail:
                    critere["erreur"].append(
                        ("""<li><p>Dans le contexte suivant :</p>"""
                        """<p>"""
                        f"""<code>python3 {options[1][-10:]} {options[2]}</code></p>"""
                        """<p>L'erreur suivante a été soulevée : </p>"""
                        """<pre class="language-python">"""
                        f"""<code>{err}</code></pre></li>"""))
                elif testEchoue:
                    print(f'{FAIL}        Erreur inattendue{ENDC}')
                    critere["erreur"].append(
                        ("""<li><p>Dans le contexte suivant :</p>"""
                         """<p>"""
                         f"""<code>python3 {options[1][-10:]} {options[2]}</code></p>"""
                         """<p>Une erreur inattendue a été soulevée</p></li>"""))
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
        critere["note"] = int(ceil(note))
        globalRes += int(ceil(note))
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
