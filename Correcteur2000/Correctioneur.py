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
from subprocess import PIPE, Popen
from difflib import SequenceMatcher
import datetime
from tests import Tests
# pyEnv = __import__('SuperCorrecteur2000').AssistantCorrection.PYENVNAME
pyEnv = "python3.7"


class CorrecteurTeam:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        self.filesCorrecteur = glob.iglob(self.projectPath)
        self.dictCritere = None

    def cleanAvantNouvelEleve(self):
        """ Supprime les fichiers crées par le code de l'élève
            afin de ne pas interferer avec le suivant
        """
        for files in glob.iglob(self.projectPath):
            if files not in self.filesCorrecteur:
                try:
                    os.remove(files)
                except IsADirectoryError:
                    shutil.rmtree(files)

    def load_correction_dict(self, pathJson):
        """
        [
        {"Critère1":
            {"Nom Test1":
                {"description " : "Description du test pour le rapport"
                 "commentaireEchec" : "Description de l'echec"
                 "Arguments":
                    {
                    [Liste d'arguments à faire en ligne de commandes]
                    }
                 "resultatAttendu": "Un mot que l'on veut matcher ou une regex"
                 "erreurAttendu": "Un mot que l'on veut matcher ou une regex"
                 "pondération" : int ou [int] pour pondérer le resultat.
                }
            }
            {"Nom Test2" :
                ........
            }
        },
        {"Critère2": ........
        }
        ]
        """
        with open(pathJson) as jsonFile:
            self.dictCritere = json.load(jsonFile)

    def corrige(self, team):
        for critere in self.dictCritere:
            commandesToTest = critere["command"]
            reAttendu = [re.compile(resAtt, flags=re.MULTILINE)
                         for resAtt in critere["resultatAttendu"]]
            reErrAttendu = [re.compile(errAtt, flags=re.MULTILINE)
                            for errAtt in critere["erreurAttendu"]]

            nomCommandeTeam = team.sorties[critere["critere"]][critere["nom"]]
            nomCommandeTeam["ponderation"] = critere["ponderation"]
            nomCommandeTeam["description"] = critere["description"]

            for command in commandesToTest:
                options = [pyEnv, team.main] + command.strip().split(" ")

                proc = Popen(options, stdout=PIPE, stderr=PIPE,
                             encoding='utf-8')
                result, err = proc.communicate(timeout=10)
                nomCommandeTeam[command]["resultat"] = result
                nomCommandeTeam[command]["erreur"] = err
                #
                # TODO La logique de si le test est réussi ou pas
                #
                if "reussi":
                    nomCommandeTeam[command]["estReussi"] = True
                else:
                    nomCommandeTeam[command]["estReussi"] = False
                    nomCommandeTeam["commentaireEchec"] = critere["commentaireEchec"]

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
        print(f"{team_dico}")
        team.saveTeamState(False)
        return team_dico

    def corrigeFromModules(self, team, modules, classes):
        if team.noTeam == 15:
            return 0
        note = 0
        print_barre()
        print_equipe(team.noTeam)
        comment = "<h2>Évaluation du critère 3</h2>"
        comment += "<h3>Fonctionnement général</h3>"
        test = Tests(team, modules, classes)
        if test.equipeOk:
            # FAIRE TOUT LES TESTS
            test.loadClassObject()
            print_titre("Prix")
            comment += "<h4>Vérification de la méthode prix</h4><ul>"
            res = test.test_2_prix()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Déposer")
            comment += "</ul><h4>Vérification de la méthode déposer</h4><ul>"
            res = test.test_3_deposer()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.test_4_deposer()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Solde")
            comment += "</ul><h4>Vérification de la méthode solde</h4<ul>>"
            res = test.test_5_solde()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.test_6_solde()
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
            res = test.test_9_acheter()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Vendre")
            comment += "</ul><h4>Vérification de la méthode vendre</h4><ul>"
            res = test.test_10_vendre()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.test_11_vendre()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Valeur totale")
            comment += "</ul><h4>Vérification de la méthode valeur totale</h4><ul>"
            res = test.test_12_valeur_totale()
            if res[0]:
                note += 1
            comment += res[1]
            res = test.test_13_valeur_totale()
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
            res = test.test_16_valeur_des_titres()
            if res[0]:
                note += 1
            comment += res[1]
            print_titre("Titre")
            comment += "</ul><h4>Vérification de la méthode titre</h4><ul>"
            res = test.test_17_titres()
            if res[0]:
                note += 1
            comment += res[1]
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
            res = test.test_20_valeur_projetee()
            if res[0]:
                note += 1
            comment += res[1]
            # FIN DE TESTS
            print_note(note, 19)
            note_temp = note
            test.cleanUp()
            test.loadClassObject()
            tqdm.tqdm.write("\n")
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
            print_final(3, note, 29)
            test.cleanUp()
        else:
            print_warning(f"FAIL : Programme non fonctionnel")
            comment += "<p>Votre code n'est pas fonctionnel</p>"
            test.cleanUp()
        return (note, comment)
        # input()
        # team.saveTeamState()
        # print()

    def corrige_nomenclature(self, listClass, listFunc, listArg, team):
        liste_fonc_team, liste_classe_team, list_arg_team = self.show_functions(team)
        print_barre()
        print_equipe(team.noTeam)
        comment = "<h3>Nomenclature: </h3>"
        print_titre("Nomenclature des classes")
        comment = "<h4>Vérification de la nomenclature des classe</h4>"
        base = float(len(listClass) + len(listFunc) + len(listArg))
        compteur = 0
        first = True
        for classe in listClass:
            find = False
            index = 0
            for i, classe_team in enumerate(liste_classe_team):
                ratio = SequenceMatcher(None, classe, classe_team).ratio()
                if ratio == 1:
                    print_command(f"{classe}", f"{classe_team}")
                    team.dictNomenclature[classe] = classe_team
                    compteur += 1
                    find = True
                    index = i
                    break
                elif 0.75 <= ratio < 1:
                    team.dictNomenclature[classe] = classe_team
                    print_command(f"{classe}", f"{classe_team}")
                    print_failing(f"FAIL ratio: {round(ratio, 1)}")
            if not find:
                if first:
                    first = False
                    comment += "<p>Les classes suivantes sont mal nommée.</p><ul>"
                comment += f"<li><code>{classe}</code></li>"
            else:
                del liste_classe_team[index]
        if not first:
            comment += "</ul>"
            first = True
        print_titre("Nomenclature des fonctions")
        comment = "<h4>Vérification de la nomenclature des fonctions</h4>"
        for fonc in listFunc:
            find = False
            index = 0
            for i, fonc_team in enumerate(liste_fonc_team):
                ratio = SequenceMatcher(None, fonc, fonc_team).ratio()
                if ratio == 1:
                    team.dictNomenclature[fonc] = fonc_team
                    print_command(f"{fonc}", f"{fonc_team}")
                    compteur += 1
                    find = True
                    index = i
                    break
                elif 0.75 <= ratio < 1:
                    team.dictNomenclature[fonc] = fonc_team
                    print_command(f"{fonc}", f"{fonc_team}")
                    print_failing(f"FAIL ratio: {round(ratio, 1)}")
            if not find:
                if first:
                    first = False
                    comment += "<p>Les fonctions suivantes sont mal nommée.</p><ul>"
                comment += f"<li><code>{fonc}</code></li>"
            elif 0.75 <= ratio < 1:
                del liste_fonc_team[index]
        if not first:
            comment += "</ul>"
            first = True
        print_titre("Nomenclature des arguments")
        comment = "<h4>Vérification de la nomenclature des arguments</h4>"
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

    def similar_name(self, string1, string2, percent=1):
        # print(f'Équipe {self.noTeam} {string1} {string2}')
        if (string2 == string1 and
                SequenceMatcher(None,
                                string1,
                                string2).ratio() == percent):
            print('')
            return True
        return False
