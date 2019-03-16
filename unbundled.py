import zipfile
import os
import glob
import json
import shutil


@dataclass(order=True)
class Unbundled:
    TP: int
    fileName: str

    def checkZipFormatString(self):
        if len(self.fileName) > 5 and self.fileName[-4:] == '.zip':
            self.fileName = self.fileName[:-4]

    def unzip(self):
        zipfilePath = (f"./TP{noTP}/{self.fileName}.zip")
        zip = zipfile.ZipFile(zipfilePath)
        zip.extractall(".")
        zip.close()

    def checkAndCreateUnbundledDir(self):
        if not os.path.exists(f"./TP{noTP}/undbundled"):
            os.makedirs(f"./TP{noTP}/undbundled")
        bundleList = os.listdir(f"./TP{noTP}/{self.fileName}")
        for bundle in enumerate(bundleList):
            if not os.path.exists(f"./TP{noTP}/undbundled/{bundle}"):
                os.makedirs(f"./TP{noTP}/undbundled/{bundle}")
            shutil.copy2(f"./TP{noTP}/{self.fileName}/{bundle}",f"./TP{noTP}/undbundled/{bundle}")

    def unbundledFile(self):
        pathcall = os.path.join(".", TP, "unbundled", subdir, PROJECTNAME)
        bundleList = os.listdir(f"./TP{noTP}/undbundled")
        for bundleFile in enumerate(bundleList):
            options = ['hg init', f"./TP{noTP}/undbundled/{bundleFile}"] + args.strip().split(" ")
            proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
            result, err = [], []
            result, err = proc.communicate()
            if result:
                options = [f'hg unbundle "./TP{noTP}/undbundled/{bundleFile}/{bundleFile}"', f"./TP{noTP}/undbundled/{bundleFile}"] + args.strip().split(" ")
                proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
                result, err = [], []
                result, err = proc.communicate()
                if result:
                    options = [f'hg update', f"./TP{noTP}/undbundled/{bundleFile}"] + args.strip().split(" ")
                    proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
                    result, err = [], []
                    result, err = proc.communicate()
                    if result:
                        print(f'{bundleFile} Done')
        print('Unbundle Done')