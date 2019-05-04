import argparse
import glob
import json
import os
import shutil
import zipfile
import re
import numpy
import tqdm
import pickle
import _thread
import time

from Correctioneur import CorrecteurTeam
from WebJsonizer import WebJsonizer
from Team import Team
from Log import *
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
EQUIPE = 22


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
        self.pathTeams = []
        self.goodTeams = {}
        if os.path.exists(f'{self.projectBasePath}{self.projectBasePath[1:]}_Teams.save'):
            self.loadAssistant()

    def initialize_Directory(self):
        if not os.path.exists(self.projectBasePath):
            os.makedirs(self.projectBasePath)
        for folder in self.requiredDirectory:
            if not os.path.exists(self.projectBasePath+folder):
                os.makedirs(self.projectBasePath+folder)

    def initialise_Teams(self, *projectName):
        pathList = f'{self.projectBasePath}/unbundled/'
        self.pathTeams = glob.glob(f"{pathList}/*")
        print("\nCreating Teams...")
        print("\nLooking for project file...\n")
        for pathTeam in self.pathTeams:
            noTeam = int(pathTeam[-6:-3])
            self.Teams[noTeam] = Team(noTeam, pathTeam)
            boolValidation = False
            for project in projectName:
                if self.Teams[noTeam].check_If_Project_Valide(project) != 0:
                    boolValidation = True
                else:
                    boolValidation = False
            if boolValidation:
                self.goodTeams[noTeam] = self.Teams[noTeam]
            else:
                self.Teams[noTeam].validProjectName = False

    def unbundle(self, path=""):
        if path != "":
            unbundler = Unbundler(path)
        else:
            unbundler = Unbundler(self.projectBasePath)
        print("Unbundling folders... ")
        unbundler.unbundle_All_Bundles()
        print(f"Unbundling {PASS}ok{ENDC}")

    def corrigeFromJson(self, pathJson="", pathFolder=""):
        if pathFolder != "":
            correcteur8000 = CorrecteurTeam(pathFolder)
        else:
            correcteur8000 = CorrecteurTeam(self.projectBasePath)
        if pathJson != "":
            correcteur8000.loadJson(pathJson)
        else:
            correcteur8000.loadJson(f'./{self.session}{self.year}-P{self.noTP}.json')
        for team in self.Teams.values():
            if team.main:
                correcteur8000.corrige(team)
        note_moy = 0
        nb_team = len(self.Teams)
        data = {}
        for team in self.Teams.values():
            note_moy += team.rapport["1"]
        print_note(note_moy/nb_team, 100)

    def makeJsonFromSavedReport(self, critere):
        # self.loadAssistant()
        data = []
        for team in self.Teams.values():
            try:
                data.append(team.rapport[critere])
                print_passing("PASS")
            except:
                print_failing("FAIL")
        with open(f'{self.projectBasePath}/result/resultatCritere{critere}.json', 'w') as outfile:
            json.dump(date, outfile, ensure_ascii=False)

    def corrigeFromModules(self, modules, classes):
        print_wtf("\n  Correction du fonctionnement\n")
        resultat = []
        badTeam = "  Bad Team are : "
        correcteurModules = CorrecteurTeam(self.projectBasePath)
        for team in tqdm.tqdm(self.Teams.values()):
            commentaire = ""
            if True:
                if team.NoMainFile:
                    print_barre()
                    print_equipe(team.noTeam)
                    print_warning(f"  FAIL : Programme non fonctionnel 2")
                    commentaire = "<h2>Évaluation du critère 3</h2>"
                    commentaire += "<h3>Fonctionnement général</h3>"
                    commentaire += "<p>Votre code n'est pas fonctionnel, voici la liste de vos fichiers trouvé:</p><ul>"
                    for file in team.files:
                        commentaire += f"<li>{file}</li>"
                    commentaire += "</ul>"
                    commentaire += f"<h4>Résultat: 0%</h4>"
                    commentaire += f"<p><strong>La correction ainsi que la composition des message est automatisé, pour toute question ou révision veuillez commenter ce fil.</strong></p>"
                    resultat.append(
                        {'équipe': team.noTeam, 'score': 0, 'commentaires': commentaire})
                    print_final(3, 0, 100)
                else:
                    test = correcteurModules.corrigeFromModules(team, modules, classes)
                    note = test[0]
                    commentaire = test[1]
                    if note == 0:
                        badTeam += f"{team.noTeam}, "
                    if team.BadMainFile:
                        note = note - 10
                        if note < 0:
                            note = 0
                        commentaire += f"<p><strong><span style='color: #ff0000;'>Votre projet n'avait pas le bon nom, 10% on été retiré de la note.</span><strong></p>"
                    commentaire += f"<h4>Résultat: {note}%</h4>"
                    commentaire += f"<p><strong>La correction ainsi que la composition des messages est automatisé, pour toutes questions ou révision veuillez commenter ce fil.</strong></p>"
                    resultat.append({'équipe': team.noTeam, 'score': note,
                                     'commentaires': commentaire})
            tqdm.tqdm.write(" ")
        print_wtf(badTeam)
        with open('./ResultatsCritère4.json', 'w') as outfile:
            json.dump(resultat, outfile, ensure_ascii=False)

    def corrigeCommit(self, noCritere, pathJson="", pathFolder=""):
        print_wtf("\n  Correction du nombre de commit\n")
        list_ready_to_publish = []
        if pathFolder != "":
            correcteur8000 = CorrecteurTeam(pathFolder)
        else:
            correcteur8000 = CorrecteurTeam(self.projectBasePath)
        if pathJson != "":
            correcteur8000.load_correction_dict(pathJson)
        else:
            correcteur8000.load_correction_dict('./critere1.json')
        for team in tqdm.tqdm(self.Teams.values()):
            if not team.NoMainFile:
                list_ready_to_publish.append(correcteur8000.correction_commit(team, noCritere))
        with open('./ResultatsCommit.json', 'w') as outfile:
            json.dump(list_ready_to_publish, outfile, ensure_ascii=False)
        print(f'{list_ready_to_publish}')

    def corrigeNoms(self, pathDicNom, pathFolder=""):
        print_wtf("\n  Correction de la nomenclature\n")
        jsonD = {}
        with open(pathDicNom) as jsonFile:
            jsonD = json.load(jsonFile)
        list_ready_to_publish = []
        if pathFolder != "":
            correcteur8000 = CorrecteurTeam(pathFolder)
        else:
            correcteur8000 = CorrecteurTeam(self.projectBasePath)
        for team in tqdm.tqdm(self.Teams.values()):
            if True:
                if not team.NoMainFile:
                    correcteur8000.show_argparse(team)
                    # list_ready_to_publish.append(correcteur8000.corrige_nomenclature(
                    #     jsonD["action"], jsonD["arg"], team))
                # tqdm.tqdm.write("Enter pour continuer", end='')
                # input("")
        with open('./ResultatsNomencature.json', 'w') as outfile:
            json.dump(list_ready_to_publish, outfile, ensure_ascii=False)

    def corrigeHelp(self, pathFolder=""):
        print_wtf("\n  Correction de la nomenclature\n")
        list_ready_to_publish = []
        if pathFolder != "":
            correcteur8000 = CorrecteurTeam(pathFolder)
        else:
            correcteur8000 = CorrecteurTeam(self.projectBasePath)
        for team in tqdm.tqdm(self.Teams.values()):
            if True:
                if not team.NoMainFile:
                    list_ready_to_publish.append(correcteur8000.corrigeHelp(team))
                    print(list_ready_to_publish)
                # tqdm.tqdm.write("Enter pour continuer", end='')
                # input("")
        with open('./ResultatsNomencatureP3.json', 'w') as outfile:
            json.dump(list_ready_to_publish, outfile, ensure_ascii=False)

    def corrige(self, pathJson, X=0):
        lastTeam = X
        b_bug = False
        for team in tqdm.tqdm(self.Teams.values()):
            if not b_bug:
                correcteur8000 = CorrecteurTeam(self.projectBasePath)
                correcteur8000.load_correction_dict(pathJson)
                # tqdm.tqdm.write(f"Doing team {team.noTeam}")
                # try:
                    # print_ok(f"THREAD : {team.noTeam}")
                if team.noTeam > X:
                    try:
                        data = correcteur8000.corrige(team)
                        # data = team.rapport["1"]
                        with open(f'{self.projectBasePath}/result/team{team.noTeam}-resultatCritere.json', 'w') as outfile:
                            json.dump(data, outfile, ensure_ascii=False)
                        lastTeam = team.noTeam
                    except:
                        b_bug = True
                        self.corrige(pathJson, X=lastTeam)
            else:
                break

            # except:
            #     print("Error: unable to start thread")
            # correcteur8000.corrige(team)
            # correcteur8000.cleanAvantNouvelEleve()

    def get_functions(self):
        correcteur8000 = CorrecteurTeam(self.projectBasePath)
        temp = []
        with open("./temp.json", 'r')as jsonfile:
            json.loads(temp, jsonfile, ensure_ascii=False)

        try:
            lastTeam = temp[-1]["équipe"]
        except KeyError:
            lastTeam = 0

        for noTeam in self.goodTeams.keys():
            if noTeam > lastTeam:
                # print(f"Fonctions du groupe : {PASS}{noTeam}{ENDC}\n")
                for file in self.goodTeams[noTeam].files:
                    if file[-3:] == ".py":
                        # print(f"\tFichier : {WARNING}{file.split('/')[-1]}{ENDC}\n")
                        with open(file) as buff:
                            print(" ".join(x for x in buff.readlines()))
                        with open(file) as file_Python:
                            for lineNb, line in enumerate(file_Python):
                                if re.compile(r"def\s").findall(line):
                                    # print(f"Line {lineNb}: {BOLD}{line}{ENDC}")
                                    self.Teams[noTeam].functions.append((file, line, lineNb))
                                if re.compile(r"class\s").findall(line):
                                    self.Teams[noTeam].classes.append((file, line, lineNb))
                                    # print(f"Line {lineNb}: {BOLD}{line}{ENDC}")
            temp.append(
                correcteur8000.correction_qualite(self.Teams[noTeam])
            )
        result = temp
        with open("./outCritere4.json", 'w')as jsonfile:
            json.dump(result, jsonfile, ensure_ascii=False)
            # input("Press any key for next group")
            # print("\n"*3)

    def show_similarity(self, fileName, percent=80):
        list_Teams = list(self.goodTeams.copy().items())
        for noTeam1, group1 in tqdm.tqdm(list_Teams):
            print_equipe(f"\n{noTeam1}")
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
            # list_Teams.remove((noTeam1, group1))

    def get_commits(self):
        for noTeam, team in self.Teams.items():
            team.countMemberComit()
            team.saveTeamState()

    def loadAssistant(self):
        loadPath = f'{self.projectBasePath}{self.projectBasePath[1:]}.save'
        with open(loadPath, 'rb') as saved_state_file:
            self = pickle.load(saved_state_file)
        for noTeam, pathTeam in zip(self.Teams.keys(), self.pathTeams):
            self.Teams[noTeam] = Team(noTeam, pathTeam).loadTeamState()

    def fusionJson(self, critère):
        path = self.projectBasePath+"/result/"
        files = glob.glob(path+"*")
        data = []
        for file in files:
            if file[16:20] == "team":
                # temp = ""
                with open(file) as jsonFile:
                    data.append(json.load(jsonFile)[f"{critère}"])
                # print(temp)
        with open(f"{path}jsonResultCrit1.json", 'w') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False)

    def saveAssistant(self):
        savePath = f'{self.projectBasePath}{self.projectBasePath[1:]}.save'
        for no, team in self.Teams.items():
            team.saveTeamState()
        with open(savePath, 'wb') as save_state_file:
            pickle.dump(self, save_state_file)


if __name__ == "__main__":
    Assistant = AssistantCorrection("H", 19, 3)
    # Assistant.initialize_Directory()
    # Assistant.unbundle()
    # Assistant.initialise_Teams("gesport.py")
    # Assistant.fusionJson(1)
    # Assistant.corrige("./dictCritèreP3.json", 28)
    # Assistant.makeJsonFromSavedReport(1)
    # Assistant.makeJsonFromSavedReport(2)
    # Assistant.saveAssistant()
    # Assistant.loadAssistant()
    # Assistant.makeJsonFromSavedReport("1")