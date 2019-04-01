import zipfile
import os
import glob
import json
import shutil



class Unbundled:
    noTP: int
    fileName: str

    def checkZipFormatString(self):
        if len(self.fileName) > 5 and self.fileName[-4:] == '.zip':
            self.fileName = self.fileName[:-4]

    def unzip(self):
        zipfilePath = (f"./TP{self.noTP}/{self.fileName}.zip")
        zip = zipfile.ZipFile(zipfilePath)
        zip.extractall(".")
        zip.close()

    def checkAndCreateUnbundledDir(self):
        if not os.path.exists(f"./TP{self.noTP}/undbundled"):
            os.makedirs(f"./TP{self.noTP}/undbundled")
        bundleList = os.listdir(f"./TP{self.noTP}/{self.fileName}")
        for bundle in enumerate(bundleList):
            if not os.path.exists(f"./TP{self.noTP}/undbundled/{bundle}"):
                os.makedirs(f"./TP{self.noTP}/undbundled/{bundle[1]}")
            shutil.copy2(f"./TP{self.noTP}/{self.fileName}/{bundle[1]}",f"./TP{self.noTP}/undbundled/{bundle[1]}")

    def unbundledFile(self):
        # pathcall = os.path.join(".", f"TP{self.noTP}", "unbundled", subdir, PROJECTNAME)
        bundleList = os.listdir(f"./TP{self.noTP}/undbundled")
        for bundleFile in enumerate(bundleList):
            options = ['hg init', f"./TP{self.noTP}/undbundled/{bundleFile[1]}"]
            proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
            result, err = [], []
            result, err = proc.communicate()
            if result:
                options = [f'hg unbundle "./TP{self.noTP}/undbundled/{bundleFile[1]}/{bundleFile[1]}"', f"./TP{self.noTP}/undbundled/{bundleFile[1]}"]
                proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
                result, err = [], []
                result, err = proc.communicate()
                if result:
                    options = [f'hg update', f"./TP{self.noTP}/undbundled/{bundleFile[1]}"]
                    proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
                    result, err = [], []
                    result, err = proc.communicate()
                    if result:
                        print(f'{bundleFile[1]} Done')
        print('Unbundle Done')