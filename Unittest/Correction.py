import unittest
import re
import subprocess
import glob
import os
from time import sleep
from subprocess import Popen, PIPE, TimeoutExpired


class CorrectionTp1Critere3(unittest.TestCase):

    #PATH = "./"

    def setUp(self):
        #self.PATH = PATH
        self.reSymValDate = re.compile(
            "(?:[a-z]+)\([a-z]+, [0-9]{4}-[0-9]{2}-[0-9]{2}, [0-9]{4}-[0-9]{2}-[0-9]{2}\)")
        self.reDateVal = re.compile(
            "\[(?:\('[0-9]{4}-[0-9]{2}-[0-9]{2}', '[0-9]+.?[0-9]+'\)(?:, )?)+\]")
        self.reNoAnswer = re.compile("\[\]")

    def get_reponse(self, args):
        print(PATH)
        arg = ["python","./test/projet1.py"] + args.split(" ")
        proc = Popen(arg, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        result, err = proc.communicate()
        result = result.split("\n")[:-1]
        #proc = subprocess.run(arg, encoding='utf-8', stdout=PIPE)
        #result, err = proc.stdout.split("\n")[:-1], proc.stderr
        count = 0
        while len(result) <= 1 and count < 5:
            print("Api en attente")
            sleep(60.0 / 5.0)
            print("Check Api\n")
            proc.kill()
            proc = Popen(arg, stdout=PIPE, stderr=PIPE, encoding='utf-8')
            result, err = proc.communicate()
            result = result.split("\n")[:-1]
            #proc = subprocess.run(arg, stdout=PIPE, stderr=PIPE)
            #result, err = proc.stdout.split("\n")[:-1], proc.stderr
            count += 1
        return (result, err)

    def test_formatSymValDate(self):
        print("\n\ntest_formatSymValDate")
        reponse, err = self.get_reponse(
            "-v=volume -d=2018-09-21 -f=2018-12-24 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))

    def test_formatDateVal(self):
        print("\n\ntest_formatDateVal")
        reponse, err = self.get_reponse(
            "-v=volume -d=2018-09-21 -f=2018-09-24 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_UnknowSym(self):
        print("\n\ntest_UnknowSym")
        reponse, err = self.get_reponse("-d=2018-09-21 -f=2018-08-24 plop")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reNoAnswer.match(reponse[1]))

    def test_paramV(self):
        print("\n\ntest_paramV")
        reponse, err = self.get_reponse("-v=volume goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_paramD(self):
        print("\n\ntest_paramD")
        reponse, err = self.get_reponse("-d=2018-09-24 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_paramF(self):
        print("\n\ntest_paramF")
        reponse, err = self.get_reponse("-f=2018-09-24 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_paramDF(self):
        print("\n\ntest_paramDF")
        reponse, err = self.get_reponse("-d=2018-09-24 -f=2018-09-24 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_paramVF(self):
        print("\n\ntest_paramVF")
        reponse, err = self.get_reponse("-v=volume -f=2018-09-24 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_paramVD(self):
        print("\n\ntest_paramVD")
        reponse, err = self.get_reponse("-v=volume -d=2018-09-24 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_paramH(self):
        print("\n\ntest_paramH")
        reponse, err = self.get_reponse("-h")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_NoParam(self):
        print("\n\ntest_NoParam")
        reponse, err = self.get_reponse("goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reNoAnswer.match(reponse[1]))

    def test_AllParam(self):
        print("\n\ntest_AllParam")
        reponse, err = self.get_reponse(
            "-v=min -d=2018-09-21 -f=2018-09-24 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_Vferm(self):
        print("\n\ntest_Vferm")
        reponse, err = self.get_reponse("-v=fermeture -f=2018-09-24 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_Vouv(self):
        print("\n\ntest_Vouv")
        reponse, err = self.get_reponse("-v=ouverture -f=2018-09-24 goog")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_Vmin(self):
        print("\n\ntest_Vmin")
        reponse, err = self.get_reponse("-v=min -f=2018-09-24 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_Vmax(self):
        print("\n\ntest_Vmax")
        reponse, err = self.get_reponse("-v=max -f=2018-09-24 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_Vvolume(self):
        print("\n\ntest_Vvolume")
        reponse, err = self.get_reponse("-v=volume -f=2018-09-24 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))

    def test_LongArg(self):
        print("\n\ntest_LongArg")
        reponse, err = self.get_reponse(
            "--valeur=volume --fin=2018-09-24 --début=2018-09-21 goog")
        print("Réponse :\n", reponse, "\n\n")
        self.assertTrue(self.reSymValDate.match(reponse[0]))
        self.assertTrue(self.reDateVal.match(reponse[1]))


if __name__ == '__main__':
    filesDepth1 = glob.glob('*')
    dirsDepth1 = filter(lambda f: os.path.isdir(f), filesDepth1)
    for fol in dirsDepth1:
        for item in os.listdir(os.path.join("./", fol)):
            if item == "projet1.py":
                CorrectionTp1Critere3.PATH = os.path.abspath(item)
                unittest.main()


"""
python projet1.py - d = 2018 - 9 - 21 - f = 2018 - 9 - 24 goog
goog(fermeture, 2018 - 09 - 21, 2018 - 09 - 24)
[('2018-09-21', '1166.0900'), ('2018-09-24', '1173.3700')]


python projet1.py - v = volume - f = 2018 - 9 - 24 goog
goog(volume, 2018 - 09 - 24, 2018 - 09 - 24)
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
