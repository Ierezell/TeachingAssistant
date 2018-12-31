import glob
import json
import os
import re
import shutil
from subprocess import PIPE, Popen, TimeoutExpired
from math import ceil


class SuperCorrecteur2000:
    """Correcteur qui lance le programme de l'élève situé en pathToUnbundled
    et le compare au résultat noté dans le Json (arg pathToJsonTemplate).

    Doc Json :
        str Critère : nom du critère
        list[str] command : commandes à executer pour obtenir le résultat à vérfier
        str nom : nom donné au test (sera utilisé pour rédiger les commentaires)
        list[str] erreurAttendu : erreur permise ou voulue pendant la correction (regex)
        list[str] attendu : résultat que l'élève est censé retourner
        str description : Description du test (pour rédiger les commentaires)
        str commentaire : Commentaire de base pour le test (sert à rédiger les commentaires)
        list[str] sortie : Sortie du programme de l'élève (Resultat & erreurs)
        list[str] erreur : erreurs soulevées par le programme de l'élève
        list[str] mauvaisResultat : sortie console du programme de l'élève
        int note : Note pour le test
        int pondération : pondération du test

    Fonctions :
        __init__ : initialise les variables et fichiers utilisés dans le reste de la classe
        cleanResultatsEleves : supprime le dossier des résultats des élèves
        cleanResultatsSiteWeb : supprime les json à televerser sur le siteweb
        cleanToutResultats : supprime tout les résultats
        getAllGroupsNumber : renvoie une liste de tout les groupes ayant soumis
        getIncorrectGroupsNumber : renvoie une liste de tout les groupes ayant soumis un bundle incorrect
        getIncorrectGroupsPath :  renvoie une liste des chemins vers les bundles des élèves ayant soumis un bundle incorrect
        getCorrectGroupsNumber : renvoie une liste des bundles corrects
        getCorrectGroupsPath : renvoie une liste des chemins vers les bundles corrects
        getNumberSubmissions : renvoie le nombre de bundles (total)
        createResultatsSiteWeb : crée le Json pour tout les critères à téléverser sur le site
        critereToJson : crée le Json pour un seul critères
        correctBadBundles : corrige les mauvais bundle et crée un detail.json pour chaque eleve
        correctGoodBundles : corrige les bons bundle et crée un detail.json pour chaque eleve
        correctAll : corrige tout les bundles
    """

    def __init__(self, pathToJsonTemplate: str, pathToUnbundled: str,
                 nomFichierElevePython: str) -> None:
        """[summary]

        Arguments:
            pathToJsonTemplate {str} -- chemin vers le json détaillé des critères
            pathToUnbundled {str} -- chemin vers le dossier des soumissions
            nomFichierElevePython {str} -- nom du fichier à corriger pour tout les élèves

        Attributs :
            filesCorrection : liste des fichiers de correction (pour supprime ceux crée par les élèves durant la correction)
            templateJson : dictionnaire des critères
            criteres : nom des critères
            ResultSiteWeb : dictionnaire : clée critère / valeur : liste de résultats des élèves
        """

        self.pathBundlesEleves = glob.glob(f"{pathToUnbundled}/*")
        self.filesCorrection = glob.glob('./*')
        self.nomFichierElevePython = nomFichierElevePython
        self.pathToJsonTemplate = pathToJsonTemplate
        with open(pathToJsonTemplate) as file:
            self.templateJson = json.load(file)
        self.criteres = sorted(
            list(set([d['critere'] for d in self.templateJson])))
        self.ResultSiteWeb = {}
        for c in self.criteres:
            self.ResultSiteWeb[c] = []
        if not os.path.exists("./Resultats"):
            os.makedirs("./Resultats")

    def cleanResultatsEleves(self):
        shutil.rmtree('./Resultats')

    def cleanResultatsSiteWeb(self):
        for file in glob.glob("./ResultatsSiteWeb*.json"):
            os.remove(file)

    def cleanToutResultats(self):
        self.cleanResultatsSiteWeb()
        self.cleanResultatsEleves()

    def getAllGroupsNumber(self) -> list:
        return list(map(lambda x: x[-9:-6], self.pathBundlesEleves))

    def getIncorrectGroupsNumber(self) -> list:
        incorrectGroups = []
        for bundle in self.pathBundlesEleves:
            sous_repertoire = glob.glob(f"../unbundled/{bundle[-16:]}/*")
            noFileToCorrect = True
            for subdirfiles in sous_repertoire:
                if subdirfiles[30:] == self.nomFichierElevePython:
                    noFileToCorrect = False
            if noFileToCorrect:
                incorrectGroups.append(bundle[-9:-6])
        return incorrectGroups

    def getIncorrectGroupsPath(self) -> list:
        incorrectGroups = []
        for bundle in self.pathBundlesEleves:
            sous_repertoire = glob.glob(f"../unbundled/{bundle[-16:]}/*")
            noFileToCorrect = True
            for subdirfiles in sous_repertoire:
                if subdirfiles[30:] == self.nomFichierElevePython:
                    noFileToCorrect = False
            if noFileToCorrect:
                incorrectGroups.append(bundle)
        return incorrectGroups

    def getCorrectGroupsNumber(self) -> list:
        return sorted(set(self.getAllGroupsNumber()) -
                      set(self.getIncorrectGroupsNumber()))

    def getCorrectGroupsPath(self) -> list:
        correctGroups = []
        for bundle in self.pathBundlesEleves:
            sous_repertoire = glob.glob(f"../unbundled/{bundle[-16:]}/*")
            for subdirfiles in sous_repertoire:
                if subdirfiles[30:] == self.nomFichierElevePython:
                    correctGroups.append(bundle)
        return correctGroups

    def getNumberSubmissions(self) -> int:
        return len(self.pathBundlesEleves)

    def createResultatsSiteWeb(self):
        folderJsonDetail = glob.glob("./Resultats/Details/*")
        for c in self.criteres:
            Resultat = []
            for pathJsonEleve in folderJsonDetail:
                groupNb = pathJsonEleve[-8:-5]
                with open(pathJsonEleve) as infile:
                    jsonEleve = json.load(infile)
                dictResult = {'équipe': groupNb,
                              'score': 0, 'commentaires': []}
                note = 0
                for test in jsonEleve:
                    if test['critere'] == c:
                        note += test["note"]*test["ponderation"]
                        dictResult["commentaires"].append(
                            (f'Nous avons effectué un test pour : {test["nom"]}'
                             f'son but était de : {test["description"]}'))
                        if test["erreur"]:
                            dictResult["commentaires"].append(
                                (f'{test["commentaire"]}'
                                 f'Un exemple de vos erreurs : {test["erreur"][0]}'))
                        if test["mauvaisResultat"]:
                            dictResult["commentaires"].append(
                                (f'{test["commentaire"]}'
                                 f'Un exemple de votre sortie incorrecte : {test["mauvaisResultat"][0]}'))
                dictResult['score'] = note
                Resultat.append(dictResult)
            with open(f'./ResultatCritere_{c}.json', 'w') as outfile:
                json.dump(Resultat, outfile)

    def critereToJson(self, critere: str = 'All'):
        if critere == 'All':
            self.createResultatsSiteWeb()
        else:
            folderJsonDetail = glob.glob("./Resultats/Details/*")
            Resultat = []
            for pathJsonEleve in folderJsonDetail:
                groupNb = pathJsonEleve[-8:-5]
                with open(pathJsonEleve) as infile:
                    jsonEleve = json.load(infile)
                dictResult = {'équipe': groupNb,
                              'score': 0, 'commentaires': []}
                note = 0
                for test in jsonEleve:
                    if test['critere'] == critere:
                        note += test["note"]*test["ponderation"]
                        dictResult["commentaires"].append(
                            (f'Nous avons effectué un test pour : {test["nom"]}'
                             f'son but était de : {test["description"]}'))
                        if test["erreur"]:
                            dictResult["commentaires"].append(
                                (f'{test["commentaire"]}'
                                 f'Un exemple de vos erreurs : {test["erreur"][0]}'))
                        if test["mauvaisResultat"]:
                            dictResult["commentaires"].append(
                                (f'{test["commentaire"]}'
                                 f'Un exemple de votre sortie incorrecte : {test["mauvaisResultat"][0]}'))
                dictResult['score'] = note
                Resultat.append(dictResult)
            with open(f'./ResultatCritere_{critere}.json', 'w') as outfile:
                json.dump(Resultat, outfile)

    def correctBadBundles(self, nomCritere: str = 'All') -> None:
        for bundle in self.getIncorrectGroupsPath():
            groupNb = bundle[-9:-6]
            filesFound = glob.glob(f"{bundle}/*")
            dictResult = {'équipe': groupNb, 'score': 0,
                          'commentaires': (f"""<h4>Résultat critère 1</h4>"""
                                           f"""<p>Il n'y a pas de fichier gesport.py dans le dossier de votre bundle."""
                                           f"""<p>Les seuls fichiers trouvés sont :</p>"""
                                           f"""<p>{filesFound}</p>""")}
            if nomCritere == 'All':
                for c in self.criteres:
                    self.ResultSiteWeb[c].append(dictResult)
            else:
                self.ResultSiteWeb[nomCritere].append(dictResult)
            if not os.path.exists("./Resultats/ResultatsEleves"):
                os.makedirs("./Resultats/ResultatsEleves")
            pathSaveEleve = f"./Resultats/ResultatsEleves/ResultatEleves_{groupNb}.json"
            with open(pathSaveEleve, 'w') as outfile:
                json.dump(dictResult, outfile)

    def _fillCritere(self, critere: dict, err: str, result: str,
                     options: list) -> None:
        critere["sortie"].append(f"RESULT : {result}")
        critere["sortie"].append(f"ERREUR : {err}")
        reAttendu = [re.compile(resAtt, flags=re.MULTILINE)
                     for resAtt in critere["attendu"]]
        reErrAttendue = [re.compile(errAtt, flags=re.MULTILINE)
                         for errAtt in critere["erreurAttendu"]]
        if err:
            testEchoue = True
            for regArg in reErrAttendue:
                if not regArg.findall(err):
                    testEchoue = False
            if testEchoue and reErrAttendue != []:
                critere["erreur"].append(
                    ("""<li><p>Dans le contexte suivant :</p>"""
                        """<pre class="line-numbers  language-python">"""
                        f"""<code>{options}</code></pre>"""
                        """<p>L'erreur suivante a été soulevé : </p>"""
                        """<pre class="line-numbers  language-python">"""
                        f"""<code>{err}</code></pre></li>"""))
        if result:
            testEchoue = True
            for regArg in reAttendu:
                if regArg.findall(result):
                    testEchoue = False
            if testEchoue and reAttendu != []:
                critere["mauvaisResultat"].append(
                    ("""<li><p>Dans le contexte suivant :</p>"""
                        """<pre class="line-numbers  language-python">"""
                        f"""<code>{options}</code></pre>"""
                        """<p>Votre code ne soulève pas d'erreur """
                        """mais ceci n'était pas le résultat attendu :<p>"""
                        """<pre class="line-numbers  language-python">"""
                        f"""<code>{result}</code></pre></li>"""))

    def _correctCritere(self, pythonEleve: str, critere: dict) -> None:
        commandesToTest = critere["command"]
        for args in commandesToTest:
            pyEnv = "python3.7"  # Patch for window path
            options = [pyEnv, pythonEleve] + args.strip().split(" ")
            print(options)
            result, err = [], []
            proc = Popen(options, stdout=PIPE, stderr=PIPE, encoding='utf-8')
            try:
                result, err = proc.communicate(timeout=1)
            except TimeoutExpired:
                err = "Votre programme a mis plus que 1s à s'executer"
            finally:
                self._fillCritere(critere, result, err, options)

        note = (len(critere["command"]) - len(critere["erreur"])
                ) / len(critere["command"]) * critere["ponderation"]
        critere["note"] = int(ceil(note))

    def _cleanAvantNouvelEleve(self):
        for files in glob.glob('./*'):
            if files not in self.filesCorrection:
                try:
                    os.remove(files)
                except IsADirectoryError:
                    shutil.rmtree(files)

    def correctGoodBundles(self, nomCritere: str = 'All') -> None:
        if not os.path.exists("./Resultats/Details"):
            os.makedirs("./Resultats/Details")
        for pathEleve in self.getCorrectGroupsPath():
            self._cleanAvantNouvelEleve()
            with open(self.pathToJsonTemplate) as infile:
                templateEleve = json.load(infile)
            groupNb = pathEleve[-9:-6]
            for critere in templateEleve:
                pythonEleve = pathEleve+'/'+self.nomFichierElevePython
                self._correctCritere(pythonEleve, critere)
            pathDetailsEleve = f"./Resultats/Details/Details_{groupNb}.json"
            with open(pathDetailsEleve, 'w') as outfile:
                json.dump(templateEleve, outfile)
        self._cleanAvantNouvelEleve()

    def correctAll(self, nomCritere: str = 'All') -> None:
        self.correctBadBundles(nomCritere)
        self.correctGoodBundles(nomCritere)
        self.createResultatsSiteWeb()


cor = SuperCorrecteur2000('./dictCritere.json', '../unbundled', 'gesport.py')
# print(cor.pathBundlesEleves)
# print(cor.criteres)
# print(cor.ResultSiteWeb)
# print(cor.getAllGroups())
# cor.getIncorrectGroups()
cor.cleanToutResultats()
cor.correctGoodBundles()
cor._cleanAvantNouvelEleve()
# cor.showResultCritere()
# cor.critereToJson()
