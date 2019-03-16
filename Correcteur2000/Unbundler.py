import os
import zipfile
import shutil
import glob

from subprocess import PIPE, Popen, TimeoutExpired


class Unbundled:
    def __init__(self, folderName):
        self.folderName = folderName
        self.allBundlesPath = f"./{self.folderName}/{self.folderName}-bundles"

    def check_Zip_Or_Folder(self):
        if not os.path.exists(self.allBundlesPath):
            if os.path.exists(f'{self.allBundlesPath}.zip'):
                os.makedirs(self.allBundlesPath)
                with zipfile.ZipFile(self.allBundlesPath) as zipped:
                    zipped.extractall(self.allBundlesPath)

    def check_And_Create_Unbundled_Dirs(self):
        self.check_Zip_Or_Folder()
        for bundle in os.listdir(self.allBundlesPath):
            fromBundle = f"./{self.allBundlesPath}/{bundle}"
            destPath = f"./{self.folderName}/unbundled/{bundle[:-3]}"
            if not os.path.exists(destPath):
                os.makedirs(destPath)
            shutil.copy2(fromBundle, destPath)

    def check_And_Create_Unbundled_One_Dir(self, No_equipe):
        self.check_Zip_Or_Folder()
        for bundle in os.listdir(self.allBundlesPath):
            if int(bundle[7:10]) == int(No_equipe):
                fromBundle = f"./{self.allBundlesPath}/{bundle}"
                destPath = f"./{self.folderName}/unbundled/{bundle[:-3]}"
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        shutil.copy2(fromBundle, destPath)

    def unbundle_One_Bundle(self, No_equipe):
        self.check_And_Create_Unbundled_One_Dir(No_equipe)
        pathBundleFolder = f"./{self.folderName}/unbundled/"
        bundleList = glob.glob(pathBundleFolder)
        for bundle in bundleList:
            if int(bundle[7:10]) == int(No_equipe):
                options = ['hg init', f"{pathBundleFolder}/{bundle}"]
                proc = Popen(options, stdout=PIPE, stderr=PIPE,
                             encoding='utf-8')
                result, err = proc.communicate()
                if not err:
                    options = [f"hg unbundle f'{pathBundleFolder}/{bundle}'"]
                    proc = Popen(options, stdout=PIPE, stderr=PIPE,
                                 encoding='utf-8')
                    result, err = proc.communicate()
                else:
                    print("Problème avec hg init !")
                    print(f"Équipe n°{bundle[7:10]} | {bundle}")
                    print(f"Erreur : \n {err}")
                    if not err:
                        options = [f"hg update f'{pathBundleFolder}/{bundle}'"]
                        proc = Popen(options, stdout=PIPE, stderr=PIPE,
                                     encoding='utf-8')
                        result, err = proc.communicate()
                    else:
                        print("Problème avec hg unbundle !")
                        print(f"Équipe n°{bundle[7:10]} | {bundle}")
                        print(f"Erreur : \n {err}")

                        if not err:
                            print(f'{bundle} Done')
                        else:
                            print("Problème avec hg update !")
                            print(f"Équipe n°{bundle[7:10]} | {bundle}")
                            print(f"Erreur : \n {err}")
            print('Unbundle Done')

    def unbundle_All_Bundles(self):
        self.check_And_Create_Unbundled_Dirs()
        pathBundleFolder = f"./{self.folderName}/unbundled/"
        bundleList = glob.glob(pathBundleFolder)
        for bundle in bundleList:
            options = ['hg init', f"{pathBundleFolder}/{bundle}"]
            proc = Popen(options, stdout=PIPE, stderr=PIPE,
                         encoding='utf-8')
            result, err = proc.communicate()
            if not err:
                options = [f"hg unbundle f'{pathBundleFolder}/{bundle}'"]
                proc = Popen(options, stdout=PIPE, stderr=PIPE,
                             encoding='utf-8')
                result, err = proc.communicate()
            else:
                print("Problème avec hg init !")
                print(f"{bundle}")
                print(f"Erreur : \n {err}")
                if not err:
                    options = [f"hg update f'{pathBundleFolder}/{bundle}'"]
                    proc = Popen(options, stdout=PIPE, stderr=PIPE,
                                 encoding='utf-8')
                    result, err = proc.communicate()
                else:
                    print("Problème avec hg unbundle !")
                    print(f"{bundle}")
                    print(f"Erreur : \n {err}")

                    if not err:
                        print(f'{bundle} Done')
                    else:
                        print("Problème avec hg update !")
                        print(f"{bundle}")
                        print(f"Erreur : \n {err}")
        print('Unbundle Done')
