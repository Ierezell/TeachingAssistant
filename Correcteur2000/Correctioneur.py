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
from subprocess import PIPE, Popen

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
        team.saveTeamState()
        return team_dico

    def corrigeFromModules(self, team, modules):
        # Remove old Team if necessary
        # if team.pathTeam in sys.path:
        #     sys.path.remove(team.pathTeam)
        # for module in modules:
        #     try:
        #         del sys.modules[module]
        #     except KeyError:
        #         pass
        # print(sys.path)
        # sys.path.insert(0, os.path.join(os.getcwd(), team.pathTeam[2:]))
        sys.path.insert(0, team.pathTeam)
        # print(sys.path)
        modules_to_remove = []
        print(team.noTeam)
        for module in modules:
            print(f"Module : {module}")
            try:
                __import__(module)
            except ModuleNotFoundError:
                print(f"No module {module} for team {team.noTeam}")
            except ImportError as e:
                missing_module = traceback.format_exc().split('\n')[-2].split()[6][1:-1]
                modules_to_remove.append(missing_module)
                if missing_module == module:
                    print("Import circulaire !")
                else:
                    print(f"Missing_module : {missing_module}")
                    __import__(missing_module)
            except Exception:
                print(traceback.format_exc())

        for module in modules_to_remove:
            del sys.modules[module]
        for module in modules:
            try:
                del sys.modules[module]
            except KeyError:
                pass
        # sys.path.remove(os.path.join(os.getcwd(), team.pathTeam[2:]))
        sys.path.remove(team.pathTeam)
