import glob
import json
import os
import re
import shutil
import tqdm
import traceback
import sys
import inspect
from Log import *
import time
import importlib
from subprocess import PIPE, Popen, TimeoutExpired
from difflib import SequenceMatcher
import datetime
from tests import Tests
# pyEnv = __import__('SuperCorrecteur2000').AssistantCorrection.PYENVNAME
pyEnv = "python3.7"


class CorrecteurTeam:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        self.filesCorrecteur = glob.glob("./*")
        self.dictCritere = None

    def cleanAvantNouvelEleve(self):
        """ Supprime les fichiers crées par le code de l'élève
            afin de ne pas interferer avec le suivant
        """
        for files in glob.glob("./*"):
            if files not in self.filesCorrecteur:
                try:
                    os.remove(files)
                except IsADirectoryError:
                    shutil.rmtree(files)

    def load_correction_dict(self, pathJson):
        """
        [
            {
                "criterion": 1,
                "criterion_title": "Ligne de commande",
                "criterion_description": "Le programme respecte <strong>toutes</strong> les spécifications de l'énoncé concernant l'interface de la ligne de commande, dont notamment celle qui permet d'obtenir de <strong>l'aide</strong> quant au fonctionnement de cette interface."
                "test_section":
                [
                    {
                        "section_title": "Commande Help",
                        "section_description": "Vérifier l'existence de la commande <code>help</code>.",
                        "weight": 60,
                        "tests":
                        [
                            {
                                "command": "-h",
                                "success_looking": true,
                                "result_regex": "usage:",
                                "error_message": "<code>Help</code> inexistant"
                            },
                            {
                                "command": "déposer -h",
                                "success_looking": true,
                                "result_regex": "usage:",
                                "error_message": "<code>Help</code> inexistant"
                            }
                        ]
                    }
                ]
            },
            {
                Critere2
            }
        ]
        """

        with open(pathJson) as jsonFile:
            self.dictCritere = json.load(jsonFile)

    def runCommand(self, team, dicCommand, timeout=5):
        b_res = False
        c_res = ""
        reAttendu = re.compile(dicCommand["result_regex"],
                               flags=re.MULTILINE)
        command = [pyEnv, team.pathTeam+"/gesport.py"] + dicCommand["command"].split(" ")
        proc = Popen(command, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        team.testResult[dicCommand["command"]] = {}
        try:
            result, err = proc.communicate(timeout=timeout)
            print(f"Team {team.noTeam} : {dicCommand['command']} res : {result} /")
        except TimeoutExpired:
            print_failing(f"""FAIL : Timeout""")
            team.testResult[dicCommand["command"]]["pass"] = False
            team.testResult[dicCommand["command"]]["error_message"] = \
                """Votre code à mis trop de temps à s'executer.\n""" +\
                """Pour ne pas bloquer la correction automatique""" +\
                f"""nous avons limité à {timeout}s pour ce critère"""
            c_res = """Votre code n'a pas été en mesure de s'exécuter dans un délai raisonnable."""
        finally:
            team.testResult[dicCommand["command"]]["resultat"] = result
            team.testResult[dicCommand["command"]]["erreur"] = err
        if dicCommand["success_looking"]:
            if reAttendu.findall(result):
                team.testResult[dicCommand["command"]]["pass"] = True
                b_res = True
                # print_passing(f"""PASS : {dicCommand["result_regex"]}""")
            else:
                print_failing(f"""FAIL : {dicCommand["result_regex"]}""")
                c_res = dicCommand["error_message"]
                team.testResult[dicCommand["command"]]["pass"] = False
                team.testResult[dicCommand["command"]]["error_message"] =\
                    dicCommand["error_message"]
        else:
            if reAttendu.findall(err):
                b_res = True
                # print_passing(f"""PASS : {dicCommand["result_regex"]}""")
                team.testResult[dicCommand["command"]]["pass"] = True
            else:
                print_failing(f"""FAIL : {dicCommand["result_regex"]}""")
                c_res = dicCommand["error_message"]
                team.testResult[dicCommand["command"]]["pass"] = False
                team.testResult[dicCommand["command"]]["error_message"] =\
                    dicCommand["error_message"]
        return b_res, c_res

    def corrige(self, team):
        dic = {}
        print_barre()
        print_equipe(team.noTeam)
        for critere in self.dictCritere:
            note = 0.0
            # crit = None
            commentaire = ""
            commentaire = f"""<h2>Critère {critere["criterion"]}</h2>"""
            commentaire += f"""<h3>{critere["criterion_title"]}</h3>"""
            commentaire += f"""<p>{critere["criterion_description"]}</p>"""
            print_ok(f"""   CRITÈRE {critere["criterion"]}\n""")
            # nombreSousSection = len(critere["test_section"])
            for subSection in critere["test_section"]:
                commentaire += f"""<h4>{subSection["section_title"]}</h4>"""
                commentaire += f"""<p><strong>{subSection["section_description"]}</strong></p>"""
                print_titre(subSection["section_title"])
                # nombreTests = len(subSection["tests"])
                commentaire += "<ul>"
                noteSubSec = 0
                lenSubSec = len(subSection["tests"])
                for test in subSection["tests"]:
                    print_command("gesport.py", f"""{test["command"]}""")
                    b_res, c_res = self.runCommand(team, test)
                    if not b_res:
                        commentaire += f"""<li>{c_res}</li>"""
                    else:
                        noteSubSec += 1
                print_note(noteSubSec, lenSubSec)
                commentaire += "</ul>"
                note += (noteSubSec/lenSubSec)*subSection["weight"]
            commentaire += f"""<h3>Résultat: {round(note, 1)}</h3>"""
            commentaire += f"""<p><strong>La correction ainsi que la composition des messages sont automatisés, pour toutes questions ou révision veuillez commenter ce fil.</strong></p>"""
            print_final(critere["criterion"], round(note, 1), 100)
            team.rapport[f"""critere["criterion"]"""] = {
                "équipe": team.noTeam, "score": round(note, 1), "commentaires": commentaire}
            team.saveTeamState()
        return team.rapport

    def correction_commit(self, team, no_critere):
        nb_commits = team.nbCommits
        no_team = team.noTeam
        team_dico = {}
        note = 0.0
        for t in self.dictCritere:
            if t["équipe"] == no_team:
                team_dico = t
        tqdm.tqdm.write(" ")
        print_barre()
        print_equipe(no_team)
        print_titre("Vérification des commits")

        comment = "<h2>Évaluation du critère 1</h2>"
        comment += "<h3>Vérification du nombre de commits minimal</h3>"

        if nb_commits >= 5:
            print_passing(f'{nb_commits}/5')
            comment += "<p>Vous avez le nombre de commit requis.</p>"
        else:
            print_failing(f'{nb_commits}/5')
            team.notes[str(no_critere)] = 0.0
            comment += f"""<p>Vous avez fait <span style="color:  # ff0000;">{nb_commits}</span> alors que le critère exigeait un minimum de 5 commits.</p>"""
            comment += "<h4>Résultat : 0 %</h4>"
            team.notes[f"{no_critere}"] = round(note, 1)
            team_dico["score"] = round(note, 1)
            team_dico["nb_commit"] = nb_commits
            team_dico["commentaires"] = comment
            team.commentaires[f"{no_critere}"] = comment
            return team_dico
        print_titre(f"""Membre contributeur [{team_dico['nb_membres']}]""")
        comment += "<h3>Vérification des contributeurs</h3><ul>"
        for membre, commit in team.membersCommits:
            print_command(f"- {membre}", f"{commit} commits")
            comment += f"""<li>{membre} à fait {commit} commits</li>"""
        tqdm.tqdm.write(" ")
        real = float(input("\nNombre réel de membre : "))
        note = 100*(real/team_dico["nb_membres"])
        if real < team_dico["nb_membres"]:
            comment += f"""</ul><p>Selon les noms des contributeurs, seul <span style="color:  # ff0000;">{int(real)}</span> des {team_dico["nb_membres"]} membres de votre équipe ont contribué au projet.</p>"""
            print_failing(
                f"""{real} membres sur {team_dico["nb_membres"]} on fait des commits""")
        else:
            comment += f"""</ul><p>Tous les membres de votre équipe ont contribué au projet.</p>"""
            print_failing(
                f"""{real} membres sur {team_dico["nb_membres"]} on fait des commits""")
        comment += f"""<h4>Résultat : {round(note, 1)} %</h4>"""
        team.commentaires[f"{no_critere}"] = comment
        team.notes[f"{no_critere}"] = round(note, 1)
        team_dico["nb_commit"] = nb_commits
        team_dico["score"] = round(note, 1)
        team_dico["commentaires"] = comment
        team.saveTeamState(False)
        return team_dico

    def correction_qualite(self, team, no_critere=4):
        nb_commits = team.nbCommits
        team_dico = {}
        note = 0.0
        tqdm.tqdm.write(" ")
        print_barre()
        print_equipe(team.noTeam)
        print_titre("Vérification des fonctions")

        comment = "<h2>Évaluation du critère 3</h2>"
        comment += "<h3>Vérification de qualité de conception</h3>"
        if len(team.functions) < 1:
            team.notes[str(no_critere)] = 0.0
            print_passing(f'{len(team.functions)} functions')
            comment += "<p>Vous n'avez fait aucune fonction.</p>"
        if len(team.classes) < 1:
            team.notes[str(no_critere)] = 0.0
            print_passing(f'{len(team.functions)} classes')
            comment += "<p>Vous n'avez fait aucune classe.</p>"
        else:
            list_str_functions = "  \n".join(
                f"Fichier {x[0].split('/')[-1]}, ligne {x[2]} : fonction : {x[1]}" for x in team.functions)
            list_str_classes = "  \n".join(
                f"Fichier {x[0].split('/')[-1]}, ligne {x[2]} : fonction : {x[1]}" for x in team.classes)
            # print(list_str_functions)
            # print(list_str_classes)
            note = int(input("Note :"))
            print("Commentaires ? (all|nom|qte| ou custom)")
            com = input("")
            print_barre()

            if note < 80:
                if com == 'nom':
                    comment += f"""<p>La qualité est améliorable (nom de variables, nom de fonctions, noms d'arguments) </p>"""
                elif com == 'qte':
                    comment += f"""<p>Vous pourriez avoir fait plus de fonctions </p>"""
                elif com == 'all':
                    comment += f"""<p>La qualité est améliorable (nom de variables, nom de fonctions) </p>"""
                    comment += f"""<p>Vous pourriez avoir fait plus de fonctions </p>"""
                elif len(com) > 4:
                    comment += f"""<p>{com}</p>"""
                comment += f"""<p>Votre fichier comporte les fonctions suivante :  {list_str_classes}.</p>"""
                comment += f"""<p>Votre fichier comporte les classes suivante :  {list_str_classes}.</p>"""

        comment += f"""<h4>Résultat : {note} %</h4>"""
        team.notes[f"{no_critere}"] = note
        team_dico["commentaires"] = comment
        team_dico["equipe"] = team.noTeam
        team_dico["note"] = note

        team.commentaires[f"{no_critere}"] = comment
        team.saveTeamState()
        return team_dico

    def corrigeFromModules(self, team, modules, classes):
        # if team.noTeam == 15:
        #     return 0
        note = 0
        print_barre()
        print_equipe(team.noTeam)
        comment = "<h2>Évaluation du critère 3</h2>"
        comment += "<h3>Fonctionnement général</h3>"
        test = Tests(team, modules, classes)
        if test.equipeOk:
            # FAIRE TOUT LES TESTS
            test.loadClassObject()
            comment += "<h3>Fonctionnement MarchéBoursier</h3>"
            print_titre("Prix")
            comment += "<h4>Vérification de la méthode prix</h4><ul>"
            res = test.test_2_prix()
            if res[0]:
                note += 1
            comment += res[1]
            comment += "<h3>Fonctionnement Portefeuille Date: 2019-03-28</h3>"
            print_titre("Déposer")
            comment += "</ul><h4>Vérification de la méthode déposer</h4><ul>"
            res = test.test_4_deposer()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Solde")
            comment += "</ul><h4>Vérification de la méthode solde</h4><ul>"
            res = test.test_6_solde()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Acheter")
            comment += "</ul><h4>Vérification de la méthode acheter</h4><ul>"
            res = test.test_9_acheter()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Vendre")
            comment += "</ul><h4>Vérification de la méthode vendre</h4><ul>"
            res = test.test_11_vendre()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Valeur totale")
            comment += "</ul><h4>Vérification de la méthode valeur totale</h4><ul>"
            res = test.test_13_valeur_totale()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.test_16_valeur_des_titres()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Titre")
            comment += "</ul><h4>Vérification de la méthode titre</h4><ul>"
            res = test.test_18_titres()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Valeur projetée")
            comment += "</ul><h4>Vérification de la méthode valeur projetée</h4><ul>"
            res = test.test_19_valeur_projetee()
            if res[0]:
                note += 1
            comment += res[1]
            test.loadClassObject()
            comment += "<h3>Fonctionnement Portefeuille Date: Par défaut</h3><p>Notez que le portefeuille à été réinitialisé complètement</p>"
            print_titre("Déposer")
            comment += "</ul><h4>Vérification de la méthode déposer</h4><ul>"
            res = test.test_3_deposer()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Solde")
            comment += "</ul><h4>Vérification de la méthode solde</h4><ul>"
            res = test.test_5_solde()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Acheter")
            comment += "</ul><h4>Vérification de la méthode acheter</h4><ul>"
            res = test.test_7_acheter()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.test_8_acheter()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Vendre")
            comment += "</ul><h4>Vérification de la méthode vendre</h4><ul>"
            res = test.test_10_vendre()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Valeur totale")
            comment += "</ul><h4>Vérification de la méthode valeur totale</h4><ul>"
            res = test.test_12_valeur_totale()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Valeur des titres")
            comment += "</ul><h4>Vérification de la méthode valeur des titres</h4><ul>"
            res = test.test_14_valeur_des_titres()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.test_15_valeur_des_titres()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Titre")
            comment += "</ul><h4>Vérification de la méthode titre</h4><ul>"
            res = test.test_17_titres()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Valeur projetée")
            comment += "</ul><h4>Vérification de la méthode valeur projetée</h4><ul>"
            res = test.test_20_valeur_projetee()
            if res[0]:
                note += 1
            comment += res[1]
            # FIN DE TESTS
            print_note(note, 19)
            note_temp = note
            # test.cleanUp()
            test.loadClassObject()
            print_titre("LiquiditéInsuffisante")
            comment += "</ul><h4>Vérification de l'erreur LiquiditéInsuffisante</h4><ul>"
            test.erreur_0_1_depot()
            res = test.erreur_0_liquid_acheter()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("ErreurDate")
            comment += "</ul><h4>Vérification de l'erreur ErreurDate</h4><ul>"
            res = test.erreur_1_date_prix()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.erreur_2_date_déposer()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.erreur_3_date_solde()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.erreur_4_date_acheter()
            if res[0]:
                note += 1
            comment += res[1]
            test.erreur_4_1_depot()
            test.erreur_4_2_achat()
            res = test.erreur_5_date_vendre()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.erreur_6_date_valeur_totale()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.erreur_7_date_valeur_titres()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.erreur_8_date_titres()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("ErreurQuantité")
            comment += "</ul><h4>Vérification de l'erreur ErreurQuantité</h4><ul>"
            res = test.erreur_9_quantite_vendre()
            if res[0]:
                note += 1
            comment += res[1]
            comment += "</ul>"
            print_note(note-note_temp, 10)
            note = round(note*100/29, 1)
            print_final(3, note, 100)
            test.cleanUp()
        else:
            print_warning(f"  FAIL : Programme non fonctionnel 1")
            comment += "<p>Votre code n'est pas fonctionnel</p>"
            test.cleanUp()
        return (note, comment)
        # input()
        # team.saveTeamState()
        # print()

    def popenStart(self, path, command):
        options = [pyEnv, path] + command.strip().split(" ")
        proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        return proc.communicate(timeout=10)

    def corrigeHelp(self, team):
        commandToTest = True
        command = "-h"
        ns = 0
        np = 0
        nc = ''
        nbas = 0
        nbap = 0
        nbac = ''
        print_barre()
        print_equipe(team.noTeam)
        print_titre("Command d'aide\n")
        while commandToTest:
            print_command("gesport.py", command)
            tqdm.tqdm.write(" ")
            res, err = self.popenStart(team.pathTeam+"/gesport.py", command)
            ns, np, nbas, nbap, ms, mp = 0, 0, 0, 0, 0, 0
            print_passing("RESULT")
            tqdm.tqdm.write(" ")
            tqdm.tqdm.write(res)
            print_failing("ERROR")
            tqdm.tqdm.write(" ")
            tqdm.tqdm.write(err)
            note = 0
            nEntete = "<h4>Nomenclature</h4>"
            nbaEntete = "<h4>Nombre d'argument</h4>"
            mEntete = "<h4>Metavar</h4>"
            nc = ""
            nbac = ""
            mc = ""
            data = input("Nomenclature Score?: ")
            tns, tnp = 0, 0
            if data:
                tns = int(data)
                ns += tns
                data = input("Nomenclature Pondération?: ")
                if data:
                    tnp = int(data)
                    np += tnp
                else:
                    tnp = tns
                    np += tnp
            if tnp > 0 and tns < tnp:
                commentBool = True
                while commentBool:
                    tempComment = input("Commentaire?: ")
                    if tempComment:
                        nc += "<li>"+tempComment+"</li>"
                    else:
                        commentBool = False
            tnbas, tnbap = 0, 0
            data = input("Nb argument Score?: ")
            if data:
                tnbas += int(data)
                nbas += tnbas
                data = input("Nb argument Pondération?: ")
                if data:
                    tnbap += int(data)
                    nbap += tnbap
                else:
                    tnbap = tnbas
                    nbap += tnbap
            if tnbap > 0 and tnbas < tnbap:
                commentBool = True
                while commentBool:
                    tempComment = input("Commentaire?: ")
                    if tempComment:
                        nbac += "<li>"+tempComment+"</>"
                    else:
                        commentBool = False
            tms, tmp = 0, 0
            data = input("Metavar Score?: ")
            if data:
                tms = int(data)
                ms += tms
                data = input("Metavar Pondération?: ")
                if data:
                    tmp = int(data)
                    mp += tmp
                else:
                    tmp = tms
                    mp += tmp
            if tmp > 0 and tms < tmp:
                commentBool = True
                while commentBool:
                    tempComment = input("Commentaire?: ")
                    if tempComment:
                        mc += "<li>"+tempComment+"</>"
                    else:
                        commentBool = False
            print_note(((tns+tnbas+tms)/(tnp+tnbap+tmp))*100, 100)
            tempCommand = input("Next Command?: ")
            if tempCommand:
                command = tempCommand+" -h"
            else:
                commandToTest = False
        note = ((tns+tnbas+tms)/(tnp+tnbap+tmp))*100
        print_final(note, 100)
        return {'équipe': team.noTeam, 'score': note, 'commentaires': "<h3>Évaluation du critère 1</h3>"+nEntete+"<ul>"+nc+"</ul>"+nbaEntete+"<ul>"+nbac+"</ul>"+mEntete+"<ul>"+mc+"</ul>"+f"<h4>Résultat: {note}%</h4><p>Commenter le fil pour toutes questions.</p>"}

    def corrige_nomenclature(self, listAction, listArg, team):
        print_barre()
        print_equipe(team.noTeam)
        liste_action_team, list_arg_team = self.show_functions(team)
        comment = "<h4>Nomenclature: </h4>"
        print_titre("Nomenclature des actions")
        comment = "<h5>Vérification de la nomenclature des actions</h5>"
        base = float(len(listAction) + len(listArg))
        compteur = 0
        first = True
        for action in listAction:
            find = False
            index = 0
            for i, action_team in enumerate(liste_action_team):
                ratio = SequenceMatcher(None, action, action_team).ratio()
                if ratio == 1:
                    print_command(f"{action}", f"{action_team}")
                    team.dictNomenclature[action] = action_team
                    compteur += 1
                    find = True
                    index = i
                    break
                elif 0.75 <= ratio < 1:
                    team.dictNomenclature[action] = action_team
                    print_command(f"{action}", f"{action_team}")
                    print_failing(f"FAIL ratio: {round(ratio, 1)}")
            if not find:
                if first:
                    first = False
                    comment += "<p>Les actions suivantes sont mal nommée.</p><ul>"
                comment += f"<li><code>{action}</code></li>"
            else:
                del liste_action_team[index]
        if not first:
            comment += "</ul>"
            first = True
        print_titre("Nomenclature des arguments")
        comment = "<h5>Vérification de la nomenclature des arguments</h5>"
        for arg in listArg:
            find = False
            index = 0
            for i, arg_team in enumerate(list_arg_team):
                ratio = SequenceMatcher(None, arg, arg_team).ratio()
                if ratio == 1:
                    print_command(f"{arg}", f"{arg_team}")
                    compteur += 1
                    find = True
                    index = i
                    break
                elif 0.75 <= ratio < 1:
                    print_command(f"{arg}", f"{arg_team}")
                    print_failing(f"FAIL ratio: {round(ratio, 1)}")
            if not find:
                if first:
                    first = False
                    comment += "<p>Les arguments suivantes sont mal nommée.</p><ul>"
                comment += f"<li><code>{arg}</code></li>"
            else:
                del list_arg_team[index]
        score = round((15*(compteur/base)), 1)
        tqdm.tqdm.write(" ")
        print_note(score, 15)
        if not first:
            comment += "</ul>"
            first = True
        comment += f"<strong>Sous-résultat: {score} </strong>"
        team.notes["3"] = {}
        team.commentaires["3"] = {}
        team.notes["3"]["Nomenclature"] = score
        team.commentaires["3"]["Nomenclature"] = comment
        team.saveTeamState()
        return {"équipe": team.noTeam, "score": score, "commentaires": comment}

    def show_functions(self, team):
        list_class = []
        list_func = []
        list_arg = []
        for file in team.files:
            if file[-3:] == ".py":
                with open(file) as file_Python:
                    for lineNb, line in enumerate(file_Python):
                        if re.compile(r"def\s").findall(line):
                            fonc = line.split('(')[0].split()[1]
                            list_func.append(fonc)
                            args = line.split('(')[1].split(', ')
                            for arg in args:
                                list_arg.append(arg.strip().split(")")[0].split("=")[0])
                        if re.compile(r"class\s").findall(line):
                            if len(line.split('(')) == 1:
                                classe = line.split()[1][:-1]
                                list_class.append(classe)
                            else:
                                classe = line.split('(')[0].split()[1]
                                list_class.append(classe)
        return (list_func, list_class, list_arg)

    def show_argparse(self, team):
        list_action = []
        list_arg = []
        for file in team.files:
            if file[-10:] == "gesport.py":
                with open(file) as file_Python:
                    actionBool = False
                    argBool = False
                    for lineNb, line in enumerate(file_Python):
                        if actionBool:
                            actionBool = False
                            if re.compile("""(\\s*['|"]\\w+['|"])""").findall(line):
                                action = re.search(
                                    """(\\s*['|"]\\w+['|"])""", line).group(0)
                                if len(action.split('"')) > 1:
                                    action = action.split('"')[-2]
                                    print(action)
                                else:
                                    action = action.split("'")[-2]
                                    print(action)
                                list_action.append(action)
                        if re.compile("""(add_parser)""").findall(line):
                            actionBool = True
                        if re.compile("""(add_parser\\(\\s*['|"]\\w+['|"])""").findall(line):
                            actionBool = False
                            action = re.search(
                                """(add_parser\\(\\s*['|"]\\w+['|"])""", line).group(0)
                            if len(action.split('"')) > 1:
                                action = action.split('"')[-2]
                                print(action)
                            else:
                                action = action.split("'")[-2]
                                print(action)
                            list_action.append(action)
                        if argBool:
                            argBool = False
                            if re.compile("""(\\s*['|"]-\\w+['|"]\\s*,\\s*['|"]--\\w+['|"])""").findall(line):
                                action = re.search(
                                    """(\\s*['|"]-\\w+['|"]\\s*,\\s*['|"]--\\w+['|"])""", line).group(0)
                                if len(action.split('"')) > 1:
                                    action = action.split('"')[-2]
                                    print(action)
                                else:
                                    action = action.split("'")[-2]
                                    print(action)
                                list_action.append(action)
                        if re.compile("""(add_argument)""").findall(line):
                            argBool = True
                        if re.compile("""(add_argument\\(\\s*['|"]-\\w+['|"]\\s*,\\s*['|"]--\\w+['|"])""").findall(line):
                            arg = re.search(
                                """(add_argument\\(\\s*['|"]-\\w+['|"]\\s*,\\s*['|"]--\\w+['|"])""", line).group(0)
                            arg = arg.split(",")[-1]
                            if len(arg.split('"')) > 1:
                                arg = arg.split('"')[-2]
                                print(arg)
                            else:
                                arg = arg.split("'")[-2]
                                print(arg)
                            list_arg.append(arg)

        input()
        return list_action, list_arg

    def similar_name(self, string1, string2, percent=1):
        # print(f'Équipe {self.noTeam} {string1} {string2}')
        if (string2 == string1 and
                SequenceMatcher(None,
                                string1,
                                string2).ratio() == percent):
            print('')
            return True
        return False
