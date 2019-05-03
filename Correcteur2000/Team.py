import glob
import re
from subprocess import PIPE, Popen, TimeoutExpired
from Log import *
import pickle
from difflib import SequenceMatcher

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
        self.membersCommits = []
        self.nbCommits = 0
        self.files = []
        self.validProjectName = True
        self.noteTot = 0
        self.notes = {}
        self.dictNomenclature = {}
        self.commentaires = {}
        self.TooManyMainFiles = False
        self.BadMainFile = False
        self.NoMainFile = False
        self.penalites = None
        self.sorties = {}
        self.rapport = []
        self.functions = []
        self.classes = []

    def saveTeamState(self):
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
        #print(f'Équipe {self.noTeam} {string1} {string2}')
        if string2[-2:] == 'py':
            if SequenceMatcher(None, string1.lower(), string2.lower()).ratio() >= percent:
                return True
        return False

    def check_If_Project_Valide(self, projectName):
        # Verifie si le projet est présent
        exactNameBool = False
        similarFound = False
        self.files = []
        for f in glob.iglob(f'{self.pathTeam}/*'):
            self.files.append(f)
            if f.split('/')[-1] == projectName:
                self.dictNomenclature[projectName[:-3]] = f.split('/')[-1][:-3]
                exactNameBool = True
                break
            # TODO: Les 3 ligne suivante sont du a l'erreur du prof dans l'énoncé
            # elif projectName == 'marche_boursier.py' and f.split('/')[-1] == "marcheboursier.py":
            #     self.dictNomenclature[projectName[:-3]] = f.split('/')[-1][:-3]
            #     exactNameBool = True
            #     break
            else:
                if self.similar_name(projectName, f.split('/')[-1]):
                    self.dictNomenclature[projectName[:-3]] = f.split('/')[-1][:-3]
                    similarFound = True
                    break
                else:
                    similarFound = False
        if not similarFound and not exactNameBool:
            print(f"""\tNo working files found for team :""",
                  f"""{FAIL}{self.noTeam}{ENDC}\n""")
            self.NoMainFile = True
            self.BadMainFile = True
        elif similarFound and not exactNameBool:
            print(f"""\tBad named files found for team :""",
                  f"""{WARNING}{self.noTeam}{ENDC}\n""")
            self.NoMainFile = True
        self.saveTeamState()

    def countMemberComit(self):
        options = ['hg', 'id', f'{self.pathTeam}', '--num']
        proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        nb_com, err = proc.communicate(timeout=10)
        if err:
            raise RuntimeError(f'Cannot compute commit number for team {self.noTeam}')
        try:
            self.nbCommits = int(nb_com)+1
        except ValueError:
            self.nbCommits = int(nb_com[:-3])+1
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
