import glob
import re
from subprocess import PIPE, Popen, TimeoutExpired
from Log import *
import pickle
from difflib import SequenceMatcher

pyEnv = "python"  # ex : py, python, python3.7

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
        self.membersCommits = []
        self.nbCommits = 0
        self.files = []
        self.validProjectName = True
        self.noteTot = 0
        self.notes = {}
        self.commentaires = {}
        self.TooManyMainFiles = False
        self.BadMainFile = False
        self.NoMainFile = False
        self.penalites = None
        self.sorties = {}
        self.rapport = []

    def saveTeamState(self):
        print(f'{self.pathTeam}/{self.noTeam}.save')
        with open(f'{self.pathTeam}/{self.noTeam}.save', 'wb') as save_team_file:
            pickle.dump(self, save_team_file)

    def loadTeamState(self):
        with open(f'{self.pathTeam}/{self.noTeam}.save', 'rb') as saved_team_file:
            self = pickle.load(saved_team_file)
            return self


#    def fileNameReport(self):
#         if not self.validProjectName:
#             print()
#             equipe(self.noTeam)
#             titre("Fichier trouvé :")
#             for file in self.files:
#                 warning(f"        - {file}")

    def similar_name(self, string1, string2, percent=0.7):
        print(f'Équipe {self.noTeam} {string1} {string2}')
        if string2[-2] == 'py' and SequenceMatcher(None, string1.lower(), string2.lower()).ratio() >= percent:
            print('POTATO')
            return True
        return False

    def check_If_Project_Valide(self, projectName):
        # Verifie si le projet est présent
        tempBool = False
        similarFound = True
        for f in glob.iglob(f'{self.pathTeam}/*'):
            self.files.append(f.split('/')[-1])
            if f.split('/')[-1] == projectName:
                tempBool = True
            else:
                if self.similar_name(projectName, f.split('/')[-1]):
                    print(f"""\t{f.split('/')[-1]} found for team :""",
                          f"""{WARNING}{self.noTeam}{ENDC}""")
                    print(f"\tMoving {self.pathTeam}/{WARNING}{f.split('/')[-1]}{ENDC}",
                          f"to {self.pathTeam}/{PASS}{projectName}{ENDC}\n")
                    options = [
                        "mv", f"{self.pathTeam}/{f.split('/')[-1]}", f'{self.pathTeam}/{projectName}']
                    proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
                    result, err = proc.communicate(timeout=10)
                    if err:
                        print(
                            f"Impossible de changer le nom de fichier de l'équipe",
                            f" {self.noTeam}",
                            "\nÀ faire manuellement pour pouvoir run d'autre tests\n")
                else:
                    similarFound = False

        if not similarFound and not tempBool:
            print(f"""\tNo working files found for team :""",
                  f"""{FAIL}{self.noTeam}{ENDC}\n""")
            self.NoMainFile = True
            self.BadMainFile = True
            return 0
            # self.validProjectName = tempBool
            # print(f"\tTeam : {f.split('/')[-2][-6:-3]} {PASS}ok{ENDC}")
        # Sinon, cherche un fichier fonctionnel
        # potentialMainFiles = []
        # if not tempBool:
        #     print(f"\tNo {projectName} for team : {FAIL}{self.noTeam}{ENDC}")
        #     for file in self.files:
        #         if file[-2:] == "py":
        #             options = [pyEnv, f'{self.pathTeam}/{file}', '-h']
        #             # result, err = [], []
        #             proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        #             result, err = proc.communicate(timeout=10)
        #             if result and (re.compile("usage: ").findall(result)):
        #                 potentialMainFiles.append(file)
        #     # Si plus d'un fichier sort une aide
        #     if len(potentialMainFiles) > 1:
        #         print(f"""\tToo many working files found for team :""",
        #               f"""{FAIL}{self.noTeam}{ENDC}"""
        #               f"""{potentialMainFiles}\n""")
        #         self.TooManyMainFiles = True
        #     # Si un seul fichier est mauvais, renomme le
        #     elif len(potentialMainFiles) == 1:
        #         print(f"""\t{potentialMainFiles[0]} found for team :""",
        #               f"""{WARNING}{self.noTeam}{ENDC}""")
        #         print(
        #             f"\tMoving {self.pathTeam}/{WARNING}{potentialMainFiles[0]}{ENDC}",
        #             f"to {self.pathTeam}/{PASS}{projectName}{ENDC}\n")
        #         self.BadMainFile = True
        #         options = ["mv", f'{self.pathTeam}/{potentialMainFiles[0]}',
        #                    f'{self.pathTeam}/{projectName}']
        #         # result, err = [], []
        #         proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        #         result, err = proc.communicate(timeout=10)
        #         if err:
        #             print(
        #                 f"Impossible de changer le nom de fichier de l'équipe",
        #                 f" {self.noTeam}",
        #                 "\nÀ faire manuellement pour pouvoir run d'autre tests\n")
            # Aucun fichier runnable
            # else:
            #     print(f"""\tNo working files found for team :""",
            #           f"""{FAIL}{self.noTeam}{ENDC}\n""")
            #     self.NoMainFile = True
            #     return 0

    def countMemberComit(self):
        options = ['hg', 'id', f'{self.pathTeam}', '--num']
        proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        nb_com, err = proc.communicate(timeout=10)
        if err:
            raise RuntimeError(f'Cannot compute commit number for team {self.noTeam}')
        self.nbCommits = int(nb_com)+1
        options1 = ["hg", "log", "--template", "{author|person}\n",
                    f"{self.pathTeam}"]
        options2 = ["sort"]
        options3 = ["uniq", "-c"]
        options4 = ["sort", "-nr"]
        proc1 = Popen(options1, stdout=PIPE, stderr=PIPE)
        proc2 = Popen(options2, stdin=proc1.stdout, stdout=PIPE, stderr=PIPE)
        proc3 = Popen(options3, stdin=proc2.stdout, stdout=PIPE, stderr=PIPE)
        proc4 = Popen(options4, stdin=proc3.stdout, stdout=PIPE, stderr=PIPE,
                      encoding='utf-8')
        nomcomit, err = proc4.communicate(timeout=10)
        if err:
            raise RuntimeError(f'Cannot do list of comits per student for team {self.noTeam}')
        listenomcomit = [numName.strip()
                         for numName in nomcomit.split('\n')][:-1]

        self.membersCommits = [(' '.join(str_comit.split()[1:]),
                                str_comit.split()[0])
                               for str_comit in listenomcomit]
