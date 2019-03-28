import glob
from subprocess import PIPE, Popen, TimeoutExpired

from SuperCorrecteur2000 import AssistantCorrection.PYENVNAME as pyEnv


class Team:
    """
    Classe pour gérer un équipe d'étudiant.
    Attributs :
        n° equipe
        chemin vers le bundle
        a-t-elle un nom de projet valide ?
        notetotal
        notes par test / commandes
        commentaires en json
        erreurs possibles lors de la moulinette
        nom du projet (utile si invalide)s
        sorties :
        [
        {"Critère1":
            {"Nom Test1":
                {"Commande1":
                    {"estReussi" : bool pour savoir si l'élève à passé
                     "resultat": Sortie (stdout) du test
                     "erreur": "Sortie (stderr) du test"
                    }
                "commande2":
                    {......}
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

    def __init__(self, noTeam, pathTeam):
        self.noTeam = noTeam
        self.pathTeam = pathTeam
        self.validProjectName = False
        self.noteTot = 0
        self.notes = {}
        self.commentaires = {}
        self.erreurs = {}
        self.main = None
        self.penalites = None
        self.sorties = {}
        self.rapport = []

    def check_If_Project_Valide(self, projectName):
        filesFound = []
        # Verifie si le projet est présent
        for file in glob.iglob(self.pathTeam):
            filesFound.append(file)
            if file == projectName:
                self.validProjectName = True
        # Sinon, cherche un fichier fonctionnel
        if not self.validProjectName:
            self.erreurs["GoodMainNotFound"] = filesFound
            for file in filesFound:
                if file[-2:] == "py":
                    options = [pyEnv, f'{self.pathTeam}/{file}', '-h']
                    # result, err = [], []
                    proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
                    result, err = proc.communicate(timeout=10)
                projectFiles = []
                if result and ("usage: ".findall(result)):
                    projectFiles.append(file)
            if len(projectFiles) > 1:
                self.erreur["TooManyMainFiles"] = projectFiles
            elif len(projectFiles) == 1:
                self.erreur["BadMainFile"]
                self.main = projectFiles[0]
            else:
                self.erreur["NoMainFile"] = True
                return None
        else:
            self.main = projectName
