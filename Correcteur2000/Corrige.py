import glob
import os
import shutil


class Correcteur:
    fileCorrection = []
    projectBasePath = ''

    def __init__(self):
        pass

    def _cleanAvantNouvelEleve(self):
        """ Supprime les fichiers crées par le code de l'élève
            afin de ne pas interferer avec le suivant
        """
        for files in glob.glob(Correcteur.projectBasePath):
            if files not in Correcteur.fileCorrection:
                try:
                    os.remove(files)
                except IsADirectoryError:
                    shutil.rmtree(files)
