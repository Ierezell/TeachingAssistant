import json
import re
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
            """
            ma variable d'environnement est python3.7
            TODO: la changer pour toi
            """
            pyEnv = "python3.7"
            # pyEnv = "python"
            options = [pyEnv, projetpath] + args.strip().split(" ")
            print(options)
            result, err = [], []
            proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
            """
            Timeout augmenté à 10 car causait problème
            """
            result, err = proc.communicate(timeout=10)
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
                        critere["erreur"].append(
                            ("""<li><p>Dans le contexte suivant :</p>"""
                            """<pre class="line-numbers  language-python">"""
                            f"""<code>{options}</code></pre>"""
                            """<p>L'erreur suivante a été soulevé : </p>"""
                            """<pre class="line-numbers  language-python">"""
                            f"""<code>{err}</code></pre></li>"""))
                if result:
                    testEchoue = True
                    for regArg in reAttendu:
                        if regArg.findall(result):
                            testEchoue = False
                    if testEchoue and reAttendu != []:
                        critere["erreur"].append(
                            ("""<li><p>Dans le contexte suivant :</p>"""
                            f"""<pre class="line-numbers  language-python">"""
                            f"""<code>{options}</code></pre>"""
                            """<p>Votre code ne soulève pas d'erreur """
                            """mais ceci n'était pas le résultat attendu :<p>"""
                            f"""<pre class="line-numbers  language-python">"""
                            f"""<code>{result}</code></pre></li>"""))
            if critere["critere"] == "2":
                if err:
                    testEchoue = True
                    for regArg in reErrAttendue:
                        """
                        J'ai modifié la condition pour retirer le NOT
                        il ne fonctionnait pas avec ma méthode pour le critère 2
                        libre à toi à le réviser
                        """
                        if regArg.findall(err):
                            print(regArg.pattern)
                            testEchoue = False
                    if testEchoue:
                        critere["erreur"].append(
                            ("""<li><p>Dans le contexte suivant :</p>"""
                            """<li><pre class="line-numbers  language-python">"""
                            f"""<code>{options}</code></pre>"""
                            """<p>L'erreur suivante a été soulevé : </p>"""
                            """<pre class="line-numbers  language-python">"""
                            f"""<code>{err}</code></pre></li>"""))
                        critere[nbEchec]
                if result:
                    testEchoue = True
                    for regArg in reAttendu:
                        if regArg.findall(result):
                            testEchoue = False
                            """
                            Retire le succès de la liste des attendu
                            Est important pour le critère 2 puisque l'ont compare à des résultat précis
                            2 commandes pourrait donc avoir le même resultat tel que "0.00"
                            """
                            if len(regArg.pattern) > 2:
                                critere["attendu"].remove(regArg.pattern)
                                break
                    if testEchoue and reAttendu != []:
                        critere["erreur"].append(
                            ("""<li><p>Dans le contexte suivant :</p>"""
                            f"""<pre class="line-numbers  language-python">"""
                            f"""<code>{options}</code></pre>"""
                            """<p>Votre code ne soulève pas d'erreur """
                            """mais ceci n'était pas le résultat attendu :<p>"""
                            f"""<pre class="line-numbers  language-python">"""
                            f"""<code>{result}</code></pre></li>"""))
        """
        Une pondération à été fait pour chaque critère
        La note est évalué selon la pondération
        La note est ensuite majoré à l'entier près (correction mode gentil)
        """
        note = (len(critere["command"]) - len(critere["erreur"])) / len(critere["command"]) * critere["ponderation"]
        print(note)
        critere["note"] = int(ceil(note))

    return dictCritere
