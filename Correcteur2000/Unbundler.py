import os
import zipfile
import shutil
import glob

from subprocess import PIPE, Popen, TimeoutExpired

HEADER = '\033[95m'
OK = '\033[94m'
PASS = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


class Unbundler:
    def __init__(self, folderName):
        self.folderName = folderName

    def check_Zip_Or_Folder(self):
        if not os.path.exists(f"{self.folderName}-bundles"):
            if os.path.exists(f"{self.folderName}-bundles.zip"):
                with zipfile.ZipFile(f"{self.folderName}-bundles.zip") as zipd:
                    zipd.extractall(self.folderName)

    def check_And_Create_Unbundled_Dirs(self):
        self.check_Zip_Or_Folder()
        bundleFolder = f"{self.folderName}/{self.folderName}-bundles"
        for bundle in os.listdir(bundleFolder):
            fromBundle = f"./{bundleFolder}/{bundle}"
            destPath = f"./{self.folderName}/unbundled/{bundle[:-3]}"
            if not os.path.exists(destPath):
                os.makedirs(destPath)
                shutil.copy2(fromBundle, destPath)

    def unbundle_All_Bundles(self):
        print("\tChecking zip file or already created folder...")
        self.check_And_Create_Unbundled_Dirs()
        print(f"\tzip file or folder {PASS}ok{ENDC}\n")
        print("\tInit / Unbundling / Updating...")
        pathBundleFolder = f"{self.folderName}/unbundled/"
        for bundle in glob.iglob(f"{pathBundleFolder}/*"):
            nomFichierHg = bundle.split('/')[-1]
            optionsInit = ['hg', 'init', f"{bundle}"]
            procInit = Popen(optionsInit, stdout=PIPE, stderr=PIPE,
                             encoding='utf-8')
            resultInit, errInit = procInit.communicate()
            if errInit:
                print(f"{FAIL}Problème avec hg init !{ENDC}")
                print(f"{bundle}")
                print(f"Erreur : \n {WARNING}{errInit}{ENDC}")
                continue
            # Pas d'erreur avec le init on continue
            else:
                os.chdir(bundle)
                optionsUnb = ["hg", "unbundle", f'{nomFichierHg}.hg']
                procUnb = Popen(optionsUnb, stdout=PIPE, stderr=PIPE,
                                encoding='utf-8')
                resultUnb, errUnb = procUnb.communicate()
                os.chdir('../../../')
            if errUnb:
                print(f"{FAIL}Problème avec hg unbundle !{ENDC}")
                print(f"{bundle}")
                print(f"Erreur : \n {WARNING}{errUnb}{ENDC}")
                raise EnvironmentError('unbundle')
            # Pas d'erreur avec le unbundle on continue
            else:
                os.chdir(bundle)
                optionsUpdate = ["hg", "update"]
                procUpdate = Popen(optionsUpdate, stdout=PIPE, stderr=PIPE,
                                   encoding='utf-8')
                resultUpdate, errUpdate = procUpdate.communicate()
                os.chdir('../../../')
            if errUpdate:
                print(f"{FAIL}Problème avec hg update !{ENDC}")
                print(f"{bundle}")
                print(f"Erreur : \n {WARNING}{errUpdate}{ENDC}")
                raise EnvironmentError('update')
            print(f"\t\t{bundle} {PASS}ok{ENDC}")
        print(f"\tInit / Unbundling / Updating {PASS}ok{ENDC}")
