import unittest
import re
# import subprocess
# import glob
# import os
# import importlib
import sys
from time import sleep
from subprocess import Popen, PIPE


class CorrectionTp1Critere3(unittest.TestCase):

    def setUp(self):
        # self.PATH = PATH
        self.reSymValDate = re.compile(
            "(?:[a-z]+)\([a-z]+, [0-9]{4}-[0-9]{2}-[0-9]{2}, [0-9]{4}-[0-9]{2}-[0-9]{2}\)")
        self.reDateVal = re.compile(
            "\[((?:\('[0-9]{4}-[0-9]{2}-[0-9]{2}', '[0-9]+.?[0-9]+'\)(?:, )?)+)*\]")

    def get_reponse(self, args):
        arg = ["python", sys.argv[1]] + args.split(" ")
        proc = Popen(arg, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        result, err = proc.communicate()
        result = result.split("\n")[:-1]
        print(result)
        # proc = subprocess.run(arg, encoding='utf-8', stdout=PIPE)
        # result, err = proc.stdout.split("\n")[:-1], proc.stderr
        count = 0
        while len(result) <= 1 and count < 5:
            # print("Api en attente")
            sleep(60.0 / 5.0)
            # print("Check Api")
            proc.kill()
            proc = Popen(arg, stdout=PIPE, stderr=PIPE, encoding='utf-8')
            result, err = proc.communicate()
            result = result.split("\n")[:-1]

            # proc = subprocess.run(arg, stdout=PIPE, stderr=PIPE)
            # result, err = proc.stdout.split("\n")[:-1], proc.stderr
            count += 1
        return (result, err)

    def get_true_reponse(self, args):
        trueArg = ["python", "../../../Corrige.py"] + args.split(" ")
        trueProc = Popen(trueArg, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        trueResult, trueErr = trueProc.communicate()
        trueResult = trueResult.split("\n")[:-1]
        print(trueResult)
        # proc = subprocess.run(arg, encoding='utf-8', stdout=PIPE)
        # result, err = proc.stdout.split("\n")[:-1], proc.stderr
        count = 0
        while len(trueResult) <= 1 and count < 5:
            # print("\nApi en attente")
            sleep(60.0 / 5.0)
            # print("Check Api")
            trueProc.kill()
            trueProc = Popen(trueArg, stdout=PIPE,
                             stderr=PIPE, encoding='utf-8')
            trueResult, trueErr = trueProc.communicate()
            trueResult = trueResult.split("\n")[:-1]

            # proc = subprocess.run(arg, stdout=PIPE, stderr=PIPE)
            # result, err = proc.stdout.split("\n")[:-1], proc.stderr
            count += 1
            print(trueResult)
        return (trueResult, trueErr)

    def test_formatSymValDate(self):
        param = "-v=volume -d=2018-09-21 -f=2018-12-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        print()

    def test_formatDateVal(self):
        param = "-v=volume -d=2018-09-21 -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reDateVal.match(reponse[1]))
        print()

    """
    def test_UnknownSym(self):
        param = "-d=2018-09-21 -f=2018-08-24 plop"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        # self.assertRegex(self, text, expected_regex) est aussi possible
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
    """

    def test_paramV(self):
        param = "-v=volume goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_paramD(self):
        param = "-d=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_paramF(self):
        param = "-f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_paramDF(self):
        param = "-d=2018-09-24 -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_paramVF(self):
        param = "-v=volume -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_paramVD(self):
        param = "-v=volume -d=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_paramH(self):
        param = "-h"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][1:3] == truereponse[1][1:3])
        print()

    def test_NoParam(self):
        param = "goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_AllParam(self):
        param = "-v=min -d=2018-09-21 -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_Vferm(self):
        param = "-v=fermeture -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_Vouv(self):
        param = "-v=ouverture -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_Vmin(self):
        param = "-v=min -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_Vmax(self):
        param = "-v=max -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_Vvolume(self):
        param = "-v=volume -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()

    def test_LongArg(self):
        param = "--valeur=volume --fin=2018-09-24 --début=2018-09-21 goog"
        reponse, err = self.get_reponse(param)
        truereponse, trueErr = self.get_true_reponse(param)
        print("\nRéponse de l'élève :\n", reponse)
        print("Réponse Attendue :\n", truereponse)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == truereponse[0])
        self.assertTrue(reponse[1][0:2] == truereponse[1][0:2])
        print()


suite = unittest.TestLoader().loadTestsFromTestCase(CorrectionTp1Critere3)
unittest.TextTestRunner(verbosity=2).run(suite)


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
