import sys

############################################################################
#  TEST DE MOULINETTE QUI NE PEUX PAS FONCTIONNER EN PYTHON  AVEC UNITTEST #
############################################################################

filesDepth1 = glob.glob('unbundled/*/*')
dirsDepth1 = list(filter(lambda f: os.path.isdir(f), filesDepth1))
listResult = {}
listPathRemise = []
for folder in dirsDepth1:
    for file in os.listdir(os.path.join("./", folder)):
        if file == "projet1.py" or file == "Projet1.py":
            listPathRemise.append(os.path.abspath(
                os.path.join(os.path.relpath(folder), file)))
print(listPathRemise)

for fichier in listPathRemise:
    print("BWAAAAAAAAAAAAAA\nBWAAAAAAAAAAAAAA\nBWAAAAAAAAAAAAAA\n\n")
    print(fichier)

"""
arg = ["python", ] + args.split(" ")
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
"""
