import argparse
import glob
import json
import os
import shutil
import zipfile

import numpy

from Correcteur2000 import Correcteur
from Team import Team
from Unbundler import Unbundled

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

    def unbundle(self):
        unbundler = Unbundled(self.projectBasePath[2:])
        unbundler.unbundle_All_Bundles()

    def initialise_Teams(self, projectName):
        pathList = f'{self.projectBasePath}/unbundled/'
        teamList = glob.iglob(pathList)
        for team in teamList:
            noTeam = int(team[-9:-6])
            pathTeam = f'{pathList}{team}'
            self.Teams[noTeam] = Team(noTeam, pathTeam)
            self.Teams[noTeam].check_If_Project_Valide(projectName)

    def correct_Good_Bundles(self):
        for team in self.Teams:
            Correcteur.filesCorrection = glob.iglob(self.projectBasePath)
            Correcteur.projectBasePath = self.projectBasePath
            if team.isProjectNameValid:
                CorrecteurTeam = Correcteur(team)
                Correcteur._cleanAvantNouvelEleve()
                CorrecteurTeam.corrige()

# TODO : transformer ça en méthode pour AssistantCorrection
    # if noProject:
    #     critereJSON = f'<h4>Résultat critère {NOCRITERE}</h4>'
    #     dicEquipeCritereFail = {'équipe': GroupNb, 'score': 0,
    #                             'commentaires': critereJSON}
    #     dicEquipeCritereFail['commentaires'] += (
    #         f"<p>Il n'y a pas de fichier {PROJECTNAME}"
    #         f"dans le dossier de votre bundle.</p>"
    #         f"<p>Les seuls fichiers trouvés sont :</p>"
    #         f"<p>{listFilesFound}</p>")
    #     ResultSiteWeb.append(dicEquipeCritereFail)
    #     print(f"Aucun fichier {PROJECTNAME} pour le groupe : {GroupNb}")
    #     with open(f'./{TP}/ResultatsSiteWeb.json', 'w') as outfile:
    #         json.dump(ResultSiteWeb, outfile, ensure_ascii=False)
