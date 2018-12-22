import json
import re
from subprocess import PIPE, Popen
from time import sleep


def fillJson(pathJson: str, projetpath: str) -> dict:
    with open(pathJson) as jsonFile:
        dictCritere = json.load(jsonFile)
    for critere in dictCritere:
        commandesToTest = critere["command"]
        reAttendu = [re.compile(resAtt, flags=re.MULTILINE)
                     for resAtt in critere["attendu"] if resAtt != '']
        reErrAttendue = [re.compile(errAtt, flags=re.MULTILINE)
                         for errAtt in critere["erreurAttendu"]]
        print(f"\n\n{critere['nom'][4:-5]}\n\n")
        for args in commandesToTest:
            options = ["python", projetpath] + args.strip().split(" ")
            print(options)
            result, err = [], []
            proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
            result, err = proc.communicate(timeout=2)
            print("err\n", err)
            critere["sortie"].append(f"RESULT : {result}")
            critere["sortie"].append(f"ERREUR : {err}")
            if critere["critere"] == "1":
                if err:
                    testEchoue = True
                    for regArg in reErrAttendue:
                        if not regArg.findall(err):
                            testEchoue = False
                    if testEchoue:
                        critere["erreur"].append(f"<li><code>{err}</code></li>")
                if result:
                    testEchoue = True
                    for regArg in reAttendu:
                        if regArg.findall(result):
                            testEchoue = False
                    if testEchoue and reAttendu != []:
                        critere["erreur"].append(
                            ("""<p>Votre code ne soulève pas d'erreur """
                            """mais ce n'est pas le résultat attendu.<p>"""
                            f"""<li><code>{result}</code></li>"""))
            if critere["critere"] == "2":
                if err:
                    testEchoue = True
                    for regArg in reErrAttendue:
                        if not regArg.findall(err):
                            print(regArg)
                            testEchoue = False
                    if testEchoue:
                        critere["erreur"].append(f"<li><code>{err}</code></li>")
                if result:
                    testEchoue = True
                    for regArg in reAttendu:
                        if regArg.findall(result):
                            print(regArg)
                            testEchoue = False
                    if testEchoue and reAttendu != []:
                        critere["erreur"].append(
                            ("""<p>Votre code ne soulève pas d'erreur """
                            """mais ce n'est pas le résultat attendu.<p>"""
                            f"""<li><code>{result}</code></li>"""))
    return dictCritere
