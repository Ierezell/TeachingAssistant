import glob
import re
from subprocess import PIPE, Popen, TimeoutExpired
pyEnv = "python3.7"  # ex : py, python, python3.7

HEADER = '\033[95m'
OK = '\033[94m'
PASS = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


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
        self.files = []
        self.validProjectName = False
        self.noteTot = 0
        self.notes = {}
        self.commentaires = {}
        self.TooManyMainFiles = False
        self.BadMainFile = False
        self.NoMainFile = False
        self.penalites = None
        self.sorties = {}
        self.rapport = []

    def check_If_Project_Valide(self, projectName):
        # Verifie si le projet est présent
        for f in glob.iglob(f'{self.pathTeam}/*'):
            self.files.append(f.split('/')[-1])
            if f.split('/')[-1] == projectName:
                self.validProjectName = True
                #print(f"\tTeam : {f.split('/')[-2][-6:-3]} {PASS}ok{ENDC}")
        # Sinon, cherche un fichier fonctionnel
        potentialMainFiles = []
        if not self.validProjectName:
            print(f"\tNo {projectName} for team : {FAIL}{self.noTeam}{ENDC}")
            for file in self.files:
                if file[-2:] == "py":
                    options = [pyEnv, f'{self.pathTeam}/{file}', '-h']
                    # result, err = [], []
                    proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
                    result, err = proc.communicate(timeout=10)
                    if result and (re.compile("usage: ").findall(result)):
                        potentialMainFiles.append(file)
            # Si plus d'un fichier sort une aide
            if len(potentialMainFiles) > 1:
                print(f"""\tToo many working files found for team :""",
                      f"""{FAIL}{self.noTeam}{ENDC}"""
                      f"""{potentialMainFiles}\n""")
                self.TooManyMainFiles = True
            # Si un seul fichier est mauvais, renomme le
            elif len(potentialMainFiles) == 1:
                print(f"""\t{potentialMainFiles[0]} found for team :""",
                      f"""{WARNING}{self.noTeam}{ENDC}""")
                print(
                    f"\tMoving {self.pathTeam}/{WARNING}{potentialMainFiles[0]}{ENDC}",
                    f"to {self.pathTeam}/{PASS}{projectName}{ENDC}\n")
                self.BadMainFile = True
                options = ["mv", f'{self.pathTeam}/{potentialMainFiles[0]}',
                           f'{self.pathTeam}/{projectName}']
                # result, err = [], []
                proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
                result, err = proc.communicate(timeout=10)
                if err:
                    print(
                        f"Impossible de changer le nom de fichier de l'équipe",
                        f" {self.noTeam}",
                        "\nÀ faire manuellement pour pouvoir run d'autre tests\n")
            # Aucun fichier runnable
            else:
                print(f"""\tNo working files found for team :""",
                      f"""{FAIL}{self.noTeam}{ENDC}\n""")
                self.NoMainFile = True
                return 0
