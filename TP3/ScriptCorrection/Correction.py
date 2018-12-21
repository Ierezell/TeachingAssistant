import glob
from fillJsonTemplate import fillJson
import json
filesDepth1 = glob.glob('../unbundled/*')
print(f"""Nombre de bundles au total : {len(filesDepth1)}""")
ResultJson1 = []
ResultJson2 = []
correctfile = 0
for bundles in filesDepth1:
    GroupNb = bundles[-9:-6]
    subdir = bundles[-16:]
    sous_repertoire = glob.glob(f"../unbundled/{subdir}/*")
    dicEquipeCritere1 = {'équipe': GroupNb, 'score': 0,
                         'commentaires': '<h4>Résultat critère 1</h4>'}
    dicEquipeCritere2 = {'équipe': GroupNb, 'score': 0,
                         'commentaires': '<h4>Résultat critère 2</h4>'}
    noGesport = True
    listFilesFound = []
    for subdirname in sous_repertoire:
        filename = subdirname[30:]
        listFilesFound.append(filename)
        if filename == "gesport.py":
            correctfile += 1
            noGesport = False
            if GroupNb == '052':
                dictDetail = fillJson('./dictCritere.json', subdirname)
                with open('Untitled-1.json', 'w') as outfile:
                    json.dump(dictDetail, outfile)

    if noGesport:
        dicEquipeCritere1['commentaires'] += (
            f"""<p>Il n'y a pas de fichier gesport.py dans le dossier de votre bundle.</p>"""
            f"""<p>Les seuls fichiers trouvés sont :</p>"""
            f"""<p>{listFilesFound}</p>""")
        print(f"Aucun fichier gesport.py pour le groupe : {GroupNb}")
    ResultJson1.append(dicEquipeCritere1)
# print(ResultJson1)
# print(ResultJson2)

# for dirname, dirnames, filenames in os.walk('../unbundled/'):
#     # print path to all subdirectories first.
#     print(dirname)
#     for subdirname in dirnames:
#         print(os.path.join(dirname, subdirname))

#     # print path to all filenames.
#     for filename in filenames:
#         print(os.path.join(dirname, filename))
