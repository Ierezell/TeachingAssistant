import sys
import re
import glob
import os
import json

ResDetail = re.compile("Res_Detail_([0-9]{3})\.txt")
Resume = re.compile("Resume_([0-9]{3})\.txt")
filesDepth1 = glob.glob('../unbundled/*')
dirsDepth1 = list(filter(lambda f: os.path.isdir(f), filesDepth1))
print("Found folders : ", dirsDepth1, "\n\n")
for folder in dirsDepth1:
    for filename in os.listdir(os.path.join("./", folder)):
        path = os.path.join(os.path.join("./", folder), filename)
        if ResDetail.match(filename):
            group = ResDetail.match(filename)
            GroupNb = group.group(1)
            pathJson = folder + '/ResultatDetaille_' + str(GroupNb) + '.json'
            with open(path) as file:
                content = file.readlines()
                with open(pathJson, 'w') as fp:
                    json.dump(content, fp)
                    print("Written correctly in json : ", filename)
        if Resume.match(filename):
            group = Resume.match(filename)
            GroupNb = group.group(1)
            pathJson = folder + '/Resume_bundle_' + str(GroupNb) + '.json'
            DicJson = {"Result": None, "Traceback": None}
            with open(path) as file:
                content = file.readlines()
                DicJson["Result"] = content[-1]
                DicJson["Traceback"] = content[:-1]
                with open(pathJson, 'w') as fp:
                    json.dump(DicJson, fp)
                    print("Written correctly in json : ", filename)
