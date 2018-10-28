import unittest
import re
import subprocess
import glob
import os
import importlib
from time import sleep
from subprocess import Popen, PIPE, TimeoutExpired


class CorrectionTp1Critere3(unittest.TestCase):

    def setUp(self):
        # self.PATH = PATH
        self.reSymValDate = re.compile(
            "(?:[a-z]+)\([a-z]+, [0-9]{4}-[0-9]{2}-[0-9]{2}, [0-9]{4}-[0-9]{2}-[0-9]{2}\)")
        self.reDateVal = re.compile(
            "\[((?:\('[0-9]{4}-[0-9]{2}-[0-9]{2}', '[0-9]+.?[0-9]+'\)(?:, )?)+)*\]")

    def get_reponse(self, args):
        arg = ["python", self.PATH] + args.split(" ")
        proc = Popen(arg, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        result, err = proc.communicate()
        result = result.split("\n")[:-1]
        # proc = subprocess.run(arg, encoding='utf-8', stdout=PIPE)
        # result, err = proc.stdout.split("\n")[:-1], proc.stderr
        count = 0
        while len(result) <= 1 and count < 5:
            print("Api en attente")
            sleep(60.0 / 5.0)
            print("Check Api\n")
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
            print("Api en attente")
            sleep(60.0 / 5.0)
            print("Check Api\n")
            trueProc.kill()
            trueProc = Popen(trueArg, stdout=PIPE,
                             stderr=PIPE, encoding='utf-8')
            trueResult, trueErr = trueProc.communicate()
            trueResult = trueResult.split("\n")[:-1]

            # proc = subprocess.run(arg, stdout=PIPE, stderr=PIPE)
            # result, err = proc.stdout.split("\n")[:-1], proc.stderr
            count += 1
        return (trueResult, trueErr)

    def test_formatSymValDate(self):
        print("\n\ntest_formatSymValDate")
        param = "-v=volume -d=2018-09-21 -f=2018-12-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))

    def test_formatDateVal(self):
        print("\n\ntest_formatDateVal")
        param = "-v=volume -d=2018-09-21 -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_UnknownSym(self):
        print("\n\ntest_UnknowSym")
        param = "-d=2018-09-21 -f=2018-08-24 plop"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        # self.assertRegex(self, text, expected_regex) est aussi possible
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_paramV(self):
        print("\n\ntest_paramV")
        param = "-v=volume goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_paramD(self):
        print("\n\ntest_paramD")
        param = "-d=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_paramF(self):
        print("\n\ntest_paramF")
        param = "-f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_paramDF(self):
        print("\n\ntest_paramDF")
        param = "-d=2018-09-24 -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_paramVF(self):
        print("\n\ntest_paramVF")
        param = "-v=volume -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_paramVD(self):
        print("\n\ntest_paramVD")
        param = "-v=volume -d=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_paramH(self):
        print("\n\ntest_paramH")
        param = "-h"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_NoParam(self):
        print("\n\ntest_NoParam")
        param = "goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_AllParam(self):
        print("\n\ntest_AllParam")
        param = "-v=min -d=2018-09-21 -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_Vferm(self):
        print("\n\ntest_Vferm")
        param = "-v=fermeture -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_Vouv(self):
        print("\n\ntest_Vouv")
        param = "-v=ouverture -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_Vmin(self):
        print("\n\ntest_Vmin")
        param = "-v=min -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_Vmax(self):
        print("\n\ntest_Vmax")
        param = "-v=max -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_Vvolume(self):
        print("\n\ntest_Vvolume")
        param = "-v=volume -f=2018-09-24 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])

    def test_LongArg(self):
        print("\n\ntest_LongArg")
        param = "--valeur=volume --fin=2018-09-24 --début=2018-09-21 goog"
        reponse, err = self.get_reponse(param)
        trueReponse, trueErr = self.get_true_reponse(param)
        print("Réponse :\n", reponse, "\n\n")
        print("Vrai réponse :\n", trueReponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))
        self.assertTrue(reponse[0] == trueReponse[0])
        self.assertTrue(reponse[1][0:2] == trueReponse[1][0:2])


if __name__ == '__main__':
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
        print("BWAAAAAAAAAAAAAA\nBWAAAAAAAAAAAAAA\nBWAAAAAAAAAAAAAA\n\n\n\n")
        print(fichier)
        CorrectionTp1Critere3.PATH = fichier
        unittest.main()

"""
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
