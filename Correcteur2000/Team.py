import glob
from subprocess import PIPE, Popen, TimeoutExpired

from SuperCorrecteur2000 import AssistantCorrection.PYENVNAME as pyEnv


class Team:
    def __init__(self, noTeam, pathTeam):
        self.noTeam = noTeam
        self.pathTeam = pathTeam
        self.isProjectNameValid = False
        self.note = 0
        self.commentaires = {}
        self.erreur = {}
        self.files = []

    def check_If_Project_Valide(self, projectName):
        filesFound = []
        for file in self.pathTeam:
            filesFound.append(file)
            if file == projectName:
                self.isProjectNameValid = True
        if not self.isProjectNameValid:
            self.erreur["FileNotFound"] = filesFound

    def project_Alternate_Name(self):
        fileFound = []
        for file in self.erreur.get("FileNotFound"):
            if file[-2:] == "py":
                options = [pyEnv, f'{self.pathTeam}/{file}', '-h']
                # result, err = [], []
                proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
                result, err = proc.communicate(timeout=10)
            if result:
                if "usage: ".findall(result):
                    fileFound.append(file)
        if len(fileFound) > 1:
            self.erreur["TooManyMainFiles"] = fileFound
        elif len(fileFound) == 1:
            return fileFound[0]
        else:
            self.erreur["NoMain"] = "No alternate valid file found"

    def nothing_To_Correct_Comment(self, critere):
        self.commentaires[critere] =
