import unittest
import re
import sys
from time import sleep
from subprocess import Popen, PIPE


class CorrectionTp1Critere3(unittest.TestCase):
    def __init__(self, testname, arg):
        super(CorrectionTp1Critere3, self).__init__(testname)
        self._arg = arg

    def setUp(self):
        # self.PATH = PATH
        self.tests = []
        self.reSymValDate = re.compile(
            "(?:[a-z]+)\([a-z]+, [0-9]{4}-[0-9]{2}-[0-9]{2}, [0-9]{4}-[0-9]{2}-[0-9]{2}\)")
        self.reDateVal = re.compile(
            "\[((?:\('[0-9]{4}-[0-9]{2}-[0-9]{2}', '[0-9]+.?[0-9]+'\)(?:, )?)+)*\]")

    def get_reponse(self, args):
        arg = ["python", sys.argv[1]] + args.split(" ")
        proc = Popen(arg, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        result, err = proc.communicate()
        result = result.split("\n")[:-1]
        # proc = subprocess.run(arg, encoding='utf-8', stdout=PIPE)
        # result, err = proc.stdout.split("\n")[:-1], proc.stderr
        count = 0
        while len(result) <= 1 and count < 5:
            #print("Api en attente")
            sleep(60.0 / 5.0)
            #print("Check Api")
            proc.kill()
            proc = Popen(arg, stdout=PIPE, stderr=PIPE, encoding='utf-8')
            result, err = proc.communicate()
            result = result.split("\n")[:-1]

            # proc = subprocess.run(arg, stdout=PIPE, stderr=PIPE)
            # result, err = proc.stdout.split("\n")[:-1], proc.stderr
            count += 1
        return (result, err)

    def get_true_reponse(self, args):
        trueArg = ["python", "./prof/Corrige.py"] + args.split(" ")
        trueProc = Popen(trueArg, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        trueResult, trueErr = trueProc.communicate()
        trueResult = trueResult.split("\n")[:-1]

        # proc = subprocess.run(arg, encoding='utf-8', stdout=PIPE)
        # result, err = proc.stdout.split("\n")[:-1], proc.stderr
        count = 0
        while len(trueResult) <= 1 and count < 5:
            #print("\nApi en attente")
            sleep(60.0 / 5.0)
            #print("Check Api")
            trueProc.kill()
            trueProc = Popen(trueArg, stdout=PIPE,
                             stderr=PIPE, encoding='utf-8')
            trueResult, trueErr = trueProc.communicate()
            trueResult = trueResult.split("\n")[:-1]

            # proc = subprocess.run(arg, stdout=PIPE, stderr=PIPE)
            # result, err = proc.stdout.split("\n")[:-1], proc.stderr
            count += 1
        return (trueResult, trueErr)

    def test_formatDateVal(self):
        param = "-v=volume -d=2018-09-21 -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_params(self):
        print("\n\narg:", self._arg)
        param = self._arg
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("Réponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        print("Erreur de l'élève :\n", err)
        print("Erreur Attendue :\n", trueErr)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])

params = ["-v=volume goog",
          "-d=2018-09-24 goog",
          "-f=2018-09-24 goog",
          "-d=2018-09-24 -f=2018-09-24 goog",
          "-v=volume -f=2018-09-24 goog",
          "-v=volume -d=2018-09-24 goog",
          "-h",
          "goog",
          "-v=min -d=2018-09-21 -f=2018-09-24 goog",
          "-v=fermeture -f=2018-09-24 goog",
          "-v=ouverture -f=2018-09-24 goog",
          "-v=min -f=2018-09-24 goog",
          "-v=max -f=2018-09-24 goog",
          "-v=volume -f=2018-09-24 goog",
          "--valeur=volume --fin=2018-09-24 --début=2018-09-21 goog"]


import HtmlTestRunner
testRunner=HtmlTestRunner.HTMLTestRunner(output="./")


suite = unittest.TestSuite()
suite.addTest(CorrectionTp1Critere3('test_formatDateVal',None))
for param in params:
    suite.addTest(CorrectionTp1Critere3('test_params', param))
unittest.testRunner(verbosity=2).run(suite)


"""
############################################################################
#  TEST DE MOULINETTE QUI NE PEUX PAS FONCTIONNER EN PYTHON  AVEC UNITTEST #
############################################################################

filesDepth1 = glob.glob('soumissions/*')
dirsDepth1 = list(filter(lambda f: os.path.isdir(f), filesDepth1))
listResult = {}
listPathRemise = []
for folder in dirsDepth1:
    for file in os.listdir(os.path.join("./", folder)):
        if file == "projet1.py":
            listPathRemise.append(os.path.abspath(
                os.path.join(os.path.relpath(folder), file)))
print(listPathRemise)

for fichier in listPathRemise:
    print("BWAAAAAAAAAAAAAA\nBWAAAAAAAAAAAAAA\nBWAAAAAAAAAAAAAA\n\n")
    print(fichier)
    CorrectionTp1Critere3.PATH = fichier
    unittest.main()


###################################
## DOCUMENTATION SUR LE PROJET 1 ##
###################################
python projet1.py -d=2018-09-21 -f=2018-09-24 goog
 >>> goog(fermeture, 2018 - 09 - 21, 2018 - 09 - 24)
    [('2018-09-21', '1166.0900'), ('2018-09-24', '1173.3700')]


python projet1.py - v = volume - f = 2018 - 9 - 24 goog
 >>> goog(volume, 2018-09-24, 2018-09-24)
    [('2018-09-24', '1271017')]


{}({},              {},       {})
symbole(valeurdesiree   datedebut datefin)

Par défaut de spécifier la valeur désirée, votre programme doit
présumer que l'utilisateur veut la valeur à la fermeture(v=fermeture).
Par défaut de spécifier une date de début, votre programme doit
présumer que l'utilisateur veut la date de fin. Par défaut de préciser
une date de fin, votre programme doit présumer que l'utilisateur veut
la date d'aujourd'hui.
pass
"""
