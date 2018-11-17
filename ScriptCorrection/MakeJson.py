import sys
import re
import glob
import os
import json

reBundleName = re.compile(r"Resultat_([0-9]{3})\.txt")
# +\.\narg :  (.+)$\n([a-z|A-Z]{2,5})
reTestFonctionnement = re.compile(r"test_f.+\.\.\. (\w{2,5})$\n",
                                  flags=re.MULTILINE)
reArgsRes = re.compile(r"test_p.+\.\.\. $\narg :  (.+)$\n(\w{2,5})$\n",
                       flags=re.MULTILINE)
reNote = re.compile(r"Ran (\d) test\w? in \d{3}\.\d{3}s$\n\n\w{6} \((.+)=(\d)\)$\n",
                    flags=re.MULTILINE)
reDetail = re.compile(r"arg: (.+)$\nR.+$\n (\[.*\])$\nR.+$\n (\[.+\])\nE.+:$\n((?:\s)?|(?:\s(?:.+\n)+))\nE.+$\n((?:\s)?|(?:\s(?:.+\n)+))",
                      flags=re.MULTILINE)
reRepEchoue = re.compile(r"R.+$\n (\[.*\])$\nR.+$\n (\[.*\])$\nE.+$\n(.*)$\nE.+$\n(.*)$\n",
                         flags=re.MULTILINE)
filesDepth1 = glob.glob('../unbundled/*')
dirsDepth1 = list(filter(lambda f: os.path.isdir(f), filesDepth1))
for folder in dirsDepth1:
    for filename in os.listdir(os.path.join("./", folder)):
        if reBundleName.match(filename):
            GroupNb = reBundleName.match(filename).group(1)
            pathRes = os.path.join(os.path.join("./", folder), filename)
            pathTxt = folder + '/ResultatC3_' + str(GroupNb) + '.txt'
    if not pathRes:
        raise FileNotFoundError(
            "Pas de fichier de résultats ! Veuillez lancez moulinetteCorrection.sh en premier")

    with open(pathRes) as file:
        content = file.read()
    with open(pathTxt, 'w+') as fileresults:
        testfonctionnement = reTestFonctionnement.findall(
            content)[0]

        resulteleve = reArgsRes.findall(content)
        Note = reNote.findall(content)[0]
        Details = reDetail.findall(content)
        fileresults.write("""Résultat du critère 3 :\n\n""")
        if testfonctionnement == 'ERROR':
            resError = reRepEchoue.findall(content)[0]
            fileresults.write(
                "Le premier test (-v=volume -d=2018-09-21 -f=2018-09-24 goog) à échoué,\n" +
                "Il y à peut-être une boucle infinie ou une erreur d'implémentation sur le fonctionement basique.\n\n" +
                "Votre réponse:\t\t {}\nLa réponse attendue: {}\n\n".format(
                    resError[0], resError[1]))
            if resError[2] != ' ':
                fileresults.write("\tVotre erreur:\n{}\n\tL'erreur attendue:\n{}".format(
                    resError[2], resError[3]))

        else:
            fileresults.write(
                "Vous avez passé {} tests sur {}\n\n".format(int(Note[0])-int(Note[2]), Note[0]))
            fileresults.write("Vous avez échoué les test suivants : \n\n")
            for ind, res in enumerate(resulteleve):
                if res[1] == 'FAIL' or res[1] == 'ERROR':
                    fileresults.write(res[0])
                    fileresults.write("\n")
                    fileresults.write("\tVotre réponse:\t\t {}\n\tLa réponse attendue: {}\n\n".format(
                        Details[ind][1], Details[ind][2]))
                    if Details[ind][3] != ' ':
                        fileresults.write("\tVotre erreur:\n{}\n\tL'erreur attendue:\n{}\n\n".format(
                            Details[ind][3], Details[ind][4]))
