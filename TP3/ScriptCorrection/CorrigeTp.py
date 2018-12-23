import glob
import json


class SuperCorrecteur2000:
    def __init__(self, pathToJsonTemplate: str, pathToUnbundled: str):
        self.pathBundlesEleves = glob.glob(pathToUnbundled+'/*')
        self.filesCorrection = glob.glob('./*')
        with open(pathToJsonTemplate) as file:
            templateJson = json.load(file)
            self.criteres = sorted(
                list(set([d['critere'] for d in templateJson])))
        self.ResultSiteWeb = {}
        for c in self.criteres:
            self.ResultSiteWeb[c] = []
            with open(f"./ResultatsSiteWeb_Critere{c}.json", "w") as _:
                continue

    def getIncorrectGroups(self) -> list:
        pass

    def getCorrectGroups(self) -> list:
        pass

    def getNumberSubmissions(self) -> int:
        return len(self.pathBundlesEleves)

    def getAllGroups(self) -> list:
        return list(map(lambda x: x[-9:-6], self.pathBundlesEleves))

    def getCorrectSubmissions(self) -> list:
        pass

    def correctGoodBundles(self) -> None:
        pass

    def correctBadBundles(self) -> None:
        pass

    def correctAll(self) -> None:
        pass

    def createJsonsForWebsite(self) -> None:
        pass


cor = SuperCorrecteur2000('./dictCritere.json', '../unbundled')
print(cor.pathBundlesEleves)
print(cor.criteres)
print(cor.ResultSiteWeb)
print(cor.getAllGroups())
