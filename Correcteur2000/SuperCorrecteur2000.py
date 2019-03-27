import argparse
import glob
import json
import os
import shutil
import zipfile

import numpy

from Correcteur import Correcteur
from Jsonizer import Jsonizer
from Team import Team
from Unbundler import Unbundler
from WebJsonizer import WebJsonizer

# TODO Finir linker Correction.
# TODO Finir linker quand pas de fichiers
# TODO

# TODO request pour get le zip directement depuis le site
# TODO override si précisé dans le argparse.
# TODO Check nom de fichier mal nommé avec la commande help

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


class AssistantCorrection:
    # Modifier le nom utilisé par votre environnement pour python
    PYENVNAME = "python3.7"  # ex : py, python, python3.7

    def __init__(self, noTP, session, year):
        self.noTP = noTP
        self.session = session[1].upper()
        self.year = year
        self.projectBasePath = f'./{self.session}{self.year}-P{self.noTP}'
        self.requiredDirectory = [
            "/unbundled",
            "/result"
        ]
        self.Teams = {}

    def initialize_Directory(self):
        if not os.path.exists(self.projectBasePath):
            os.makedirs(self.projectBasePath)
        for folder in self.requiredDirectory:
            if not os.path.exists(self.projectBasePath+folder):
                os.makedirs(self.projectBasePath+folder)

    def initialise_Teams(self, projectName):
        pathList = f'{self.projectBasePath}/unbundled/'
        teamList = glob.iglob(pathList)
        for team in teamList:
            noTeam = int(team[-9:-6])
            pathTeam = f'{pathList}{team}'
            self.Teams[noTeam] = Team(noTeam, pathTeam)
            self.Teams[noTeam].check_If_Project_Valide(projectName)

    def unbundle(self):
        unbundler = Unbundler(self.projectBasePath[2:])
        unbundler.unbundle_All_Bundles()

    def corrige(self, pathJson):
        correcteur8000 = Correcteur(self.projectBasePath)
        correcteur8000.loadJson(pathJson)
        for team in self.Teams:
            if team.main:
                correcteur8000.corrige(team)

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


if __name__ == "main":
    Assistant = AssistantCorrection(noTP, session, year)
    Assistant.initialize_Directory()
    Assistant.unbundle()
    Assistant.initialise_Teams("projet1.py")
    Assistant.corrige("./dictCritere.json")
    Assistant.makeRapport()
    Assistant.groupAndJsonize()
    Assistant.sendToWebsite()
