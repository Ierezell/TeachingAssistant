import glob
import json
import os
import re
import shutil
from Log import *
from subprocess import PIPE, Popen

# pyEnv = __import__('SuperCorrecteur2000').AssistantCorrection.PYENVNAME
pyEnv = "python"


class Correcteur:
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

    def correction_commit(self, pathJson, team, no_critere):
        nb_commits = team.nbCommites
        no_team = team.noTeam
        team_dico = {}
        note = 0.0
        list_comment = []
        with open(pathJson) as jsonFile:
            self.dictCritere = json.load(jsonFile)
        for t in selfdictCritere:
            if t["equipe"] == no_team:
                team_dico = t
        strip()
        equipe(no_team)
        titre("Vérification des commits")
        if nb_commits >= 5:
            passing(f'{nb_commits}/5')
            list_comment.append(f"Vous avez fait {nb_commits}")
        else:
            failing(f'{nb_commits}/5')
            team.notes[str(no_critere)] = 0.0
            list_comment.append(
                f"""Vous avez fait <span style="color:  # ff0000;">{nb_commits}</span> alors que le critère exigeait un minimum de 5 commits.""")
            team.commentaire[f"{no_critere}"] = list_comment
            team.commentaire[f"{note}"] = note
            return False
        titre(f"Membre contributeur [{team_dico["nb_membres"]}]")
        for membre, commit in team.members:
            command(f"- {membre}", f"{commit} commits")
            list_comment.append(f"""{membre} à fait {commit} commits""")
        real = float(input("Nombre réel de membre : "))
        note = 20*(real/team_dico["nb_membres"])
        if real < team_dico["nb_membres"]:
            list_comment.append(
                f"""Seulement {real} membres sur {team_dico["nb_membres"]} on fait des commits""")
            failing(
                f"""{real} membres sur {team_dico["nb_membres"]} on fait des commits""")
        else:
            list_comment.append(
                f"""Vous avez tous fait au moins 1 commit.""")
        team.commentaire[f"{no_critere}"] = list_comment
        team.commentaire[f"{note}"] = note
