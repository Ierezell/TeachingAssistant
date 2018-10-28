import unittest
import re
import subprocess
from time import sleep
from subprocess import Popen, PIPE, TimeoutExpired


class CorrectionTp1Critere3(unittest.TestCase):
    def setUp(self):
        self.reSymValDate = re.compile(
            "(?:[a-z]+)\([a-z]+, [0-9]{4}-[0-9]{2}-[0-9]{2}, [0-9]{4}-[0-9]{2}-[0-9]{2}\)")
        self.reDateVal = re.compile(
            "\[(?:\('[0-9]{4}-[0-9]{2}-[0-9]{2}', '[0-9]+.?[0-9]+'\)(?:, )?)+\]")

    def get_reponse(self, args):
        arg = ["python", "./projet1.py"] + args.split(" ")
        proc = Popen(arg, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        result, err = proc.communicate()
        result = result.split("\n")[:-1]
        #proc = subprocess.run(arg, encoding='utf-8', stdout=PIPE)
        #result, err = proc.stdout.split("\n")[:-1], proc.stderr
        while len(result) <= 1:
            print("Api en attente")
            sleep(20)
            print("Check Api\n")
            proc.kill()
            proc = Popen(arg, stdout=PIPE, stderr=PIPE, encoding='utf-8')
            result, err = proc.communicate()
            result = result.split("\n")[:-1]
            #proc = subprocess.run(arg, stdout=PIPE, stderr=PIPE)
            #result, err = proc.stdout.split("\n")[:-1], proc.stderr
        return (result, err)

    def CreateTest(self):
        




def suite():
    suite = unittest.TestSuite()
    suite.addTest(BarTestCase('test_nine'))
    suite.addTest(FooTestCase('test_ten'))
    suite.addTest(FooTestCase('test_eleven'))
    suite.addTest(BarTestCase('test_twelve'))
    return suite
Execute the test-suite, e.g.,

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
