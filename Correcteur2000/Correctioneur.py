import glob
import json
import os
import re
import shutil
import tqdm
import traceback
import sys
from Log import *
import time
import importlib
from subprocess import PIPE, Popen
from difflib import SequenceMatcher

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
        team_dico["score"] = round(note, 1)
        team_dico["commentaires"] = comment
        team.saveTeamState(False)
        return team_dico

    def corrigeFromModules(self, team, modules):
        # Remove old Team if necessary
        init_modules = sys.modules.keys()
        os.chdir(team.pathTeam)
        sys.path.insert(0, os.getcwd())
        modules_to_remove = []
        mod = [None]*len(modules)
        equipeOk = True
        print(team.noTeam)
        missing_module = None
        miss_mod = None
        for i, module in enumerate(modules):
            try:
                mod[i] = importlib.import_module(module)
                mod[i] = importlib.reload(mod[i])
            except ModuleNotFoundError:
                print(f"No module {module} for team {team.noTeam}")
                equipeOk = False
            except ImportError:
                missing_module = traceback.format_exc().split('\n')[-2].split()[6][1:-1]
                if missing_module == module:
                    print("Import circulaire !")
                    equipeOk = False
                else:
                    modules_to_remove.append(missing_module)
                    miss_mod = importlib.import_module(missing_module)
                    miss_mod = importlib.reload(miss_mod)
                    mod[i] = importlib.import_module(module)
                    mod[i] = importlib.reload(mod[i])

            except Exception:
                print(traceback.format_exc())
                equipeOk = False

        if equipeOk:
            try:
                m = mod[0].MarchéBoursier()
                # m = mod[0].MarcheBoursier()
                # m = mod[0].Marcheboursier()
                # m = mod[0].Marchéboursier()
                # m = mod[0].MarcherBoursier()
                # m = mod[0].Marcherboursier()
                p = mod[1].Portefeuille(m)
            except AttributeError as e:
                print(e)
                print("Impossible d'initialiser un marché")
                if input("Afficher le fichier ?") == 'y':
                    with open(f"marche_boursier.py", "r") as file:
                        print(file.read())
            except TypeError as e:
                print(e)
                print("Le constructeur n'accepte pas une instance de marché")
                if input("Afficher le fichier ?") == 'y':
                    with open(f"portefeuille.py", "r") as file:
                        print(file.read())
        for module in modules_to_remove:
            del sys.modules[module]
        for module in modules:
            if module in sys.modules:
                del sys.modules[module]
        for modulilou in sys.modules.keys():
            if not modulilou in init_modules:
                del(sys.modules[m])
        # sys.path.remove(os.path.join(os.getcwd(), team.pathTeam[2:]))
<<<<<<< HEAD
        sys.path.remove(team.pathTeam)

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
        team.saveTeamState(False)
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
        #print(f'Équipe {self.noTeam} {string1} {string2}')
        if (string2 == string1 and
                SequenceMatcher(None,
                                string1,
                                string2).ratio() == percent):
            print('')
            return True
        return False
=======
        sys.path.remove(os.getcwd())
        os.chdir('../../../')
        print()
>>>>>>> 5ef3d4975d522b4c14f456de5bd3631acfa72bba
