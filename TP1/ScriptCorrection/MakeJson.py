import sys
import re
import glob
import os
import json

reNote = re.compile(
    r"(Vous avez passé (\d) tests sur (\d)(?:\s?\(.+\))?$)\n", flags=re.MULTILINE)
reEchoue = re.compile(r"Le premier test", flags=re.MULTILINE)
reCommentaires = re.compile(
    r"(-\w.+\w{4}$\n)((?:.*\n)*?(?=(?:-.+\n))|(?:.+\n\n?)*)", flags=re.MULTILINE)
filesDepth1 = glob.glob('../unbundled/*/ResultatC3_*.txt')
listJson = []
moyenne = 0
nb_corrige = 0
for filename in filesDepth1:
    GroupNb = filename[-7:-4]
    dicEquipe = {'équipe': GroupNb, 'score': 0, 'commentaires': ''}
    with open(filename) as file:
        content = file.read()

    Note = reNote.findall(content)
    if Note:
        Note = Note[0]
        commentaires = reCommentaires.findall(content)
        if commentaires:
            commentaires = commentaires[0]
            dicEquipe['commentaires'] = Note[0] + " " +\
                commentaires[0]+commentaires[1]
        dicEquipe['score'] = ((1+float(Note[1]))/(float(Note[2])+1))*100

    else:
        dicEquipe['score'] = 0
        dicEquipe['commentaires'] = content[25:]
    moyenne += dicEquipe['score']
    # print(dicEquipe['score'])
    nb_corrige += 1
    listJson.append(dicEquipe)
# print(moyenne/nb_corrige)

pathJson = '../Resultats/ResultatC3.json'
with open(pathJson, 'w+') as fileJson:
    json.dump(listJson, fileJson)
