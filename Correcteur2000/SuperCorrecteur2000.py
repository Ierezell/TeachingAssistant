import argparse
import glob
import json
import os
import shutil
import zipfile
import re
import numpy
import tqdm

from Correctioneur import Correcteur
from WebJsonizer import WebJsonizer
from Team import Team
from Unbundler import Unbundler
from WebJsonizer import WebJsonizer
from subprocess import PIPE, Popen

# TODO Finir linker Correction.
# TODO Finir linker quand pas de fichiers
# TODO

# TODO request pour get le zip directement depuis le site
# TODO override si précisé dans le argparse.
# TODO Check nom de fichier mal nommé avec la commande help
HEADER = '\033[95m'
OK = '\033[94m'
PASS = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
"""
/TA:
    /H19-P1:
        H19-P1-critere.json
        /H19-P1-bundles.zip
        /H19-P1-bundles
        /unbundled
            /bundles-012
                /bundle-012.hg
                main.py
                portefeuille.py
        /result
            H19-P1-resultSiteWeb.json
            /teams
                team-001.json
                team-002.json
    /H19-P2:
        H19-P2-Critere.json
        /H19-P2-bundles.zip
        /H19-P2-bundles
        /unbundled
            /bundles-012
                /bundle-012.hg
                main.py
                portefeuille.py
        /result
            H19-P2-resultSiteWeb.json
            /teams
                team-001.json
                team-002.json
"""

PYENVNAME = "python3.7"  # ex : py, python, python3.7


class AssistantCorrection:
    # Modifier le nom utilisé par votre environnement pour python

    def __init__(self, session, year, noTP):
        self.noTP = noTP
        self.session = session.upper()
        self.year = year
        self.projectBasePath = f'./{self.session}{self.year}-P{self.noTP}'
        self.requiredDirectory = [
            "/unbundled",
            "/result"
        ]
        self.Teams = {}
        self.goodTeams = {}

    def initialize_Directory(self):
        if not os.path.exists(self.projectBasePath):
            os.makedirs(self.projectBasePath)
        for folder in self.requiredDirectory:
            if not os.path.exists(self.projectBasePath+folder):
                os.makedirs(self.projectBasePath+folder)

    def initialise_Teams(self, projectName):
        pathList = f'{self.projectBasePath}/unbundled/'
        teamList = glob.iglob(f"{pathList}/*")
        print("\nCreating Teams...")
        print("\nLooking for project file...\n")
        for pathTeam in teamList:
            noTeam = int(pathTeam[-6:-3])
            self.Teams[noTeam] = Team(noTeam, pathTeam)
            if self.Teams[noTeam].check_If_Project_Valide(projectName) != 0:
                self.goodTeams[noTeam] = self.Teams[noTeam]

    def unbundle(self, path=""):
        if path != "":
            unbundler = Unbundler(path)
        else:
            unbundler = Unbundler(self.projectBasePath)
        print("Unbundling folders... ")
        unbundler.unbundle_All_Bundles()
        print(f"Unbundling {PASS}ok{ENDC}")

    def corrige(self, pathJson):
        correcteur8000 = Correcteur(self.projectBasePath)
        correcteur8000.loadJson(pathJson)
        for team in self.Teams:
            if team.main:
                correcteur8000.corrige(team)

    def show_functions(self):
        for noTeam, team in self.goodTeams:
            print(f"Fonctions du groupe : {PASS}{noTeam}{ENDC}\n")
            for file in team.files:
                if file[-3:] == ".py":
                    print(f"\tFichier : {WARNING}{file.split('/')[-1]}{ENDC}\n")
                    with open(file) as file_Python:
                        for lineNb, line in enumerate(file_Python):
                            if re.compile(r"def\s").findall(line):
                                print(f"Line {lineNb}: {BOLD}{line}{ENDC}")
            input("Press enter for next group")
            print("\n\n")

    def show_similarity(self, fileName, percent=80):
        list_Teams = list(self.goodTeams.copy().items())
        for noTeam1, group1 in tqdm.tqdm(list_Teams):
            file_group1 = f"{group1.pathTeam}/{fileName}"
            for noTeam2, group2 in list_Teams:
                file_group2 = f"{group2.pathTeam}/{fileName}"
                options = ['pycode_similar', file_group1, file_group2]
                proc = Popen(options, stdout=PIPE, stderr=PIPE,
                             encoding='utf-8')
                result, err = proc.communicate(timeout=10)
                try:
                    r = float(re.compile(r"\d?\d?\d\.\d\d").findall(result)[0])
                except IndexError:
                    continue
                if r >= percent and noTeam1 != noTeam2:
                    tqdm.tqdm.write(
                        f"{BOLD}ÉQUIPE{ENDC} {PASS}{noTeam1}{ENDC} {BOLD}Et{ENDC} {PASS}{noTeam2}{ENDC} {FAIL} {r} %{ENDC}")
            list_Teams.remove((noTeam1, group1))

    def makeRapports(self):
        webJsonMaker = WebJsonizer()
        for team in self.Teams:
            webJsonMaker.makeRapport(team)

    def groupAndJsonize(self):
        webJsonMaker = WebJsonizer()
        webJsonMaker.jsonizeResults(self.Teams)

    def sendToWebsite(self):
        # request blabla url python post data json
        pass


if __name__ == "__main__":
    Assistant = AssistantCorrection("H", 19, 2)
    Assistant.initialize_Directory()
    Assistant.unbundle()
    Assistant.initialise_Teams("projet1.py")
    # Assistant.show_functions()
    Assistant.show_similarity("projet1.py")
    # Assistant.corrige("./dictCritere.json")
    # Assistant.makeRapport()
    # Assistant.groupAndJsonize()
    # Assistant.sendToWebsite()
