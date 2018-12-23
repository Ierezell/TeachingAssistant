import json
import glob

jsonEleves = glob.glob('./Resultats/*')

# "SOIT AVOIR EN REGEX : 1 x 'STRING,' 2 x 'FLOAT,' 1 x 'BOOL,' 1 x 'DATE,' 1 x 'STRING [STRING'","OU D'AVOIR : 1 x 'INT,'"


def AddEleveResultSiteWeb(pathJsonEleve: str) -> None:
    GroupNb = pathJsonEleve[-8:-5]
    with open(pathJsonEleve) as infile:
        dictResultEleve = json.load(infile)
    criteres = sorted(list(set([d['critere'] for d in dictResultEleve])))
    notes = [{c: 0} for c in criteres]
    commentaires = [{c: []} for c in criteres]
    for i, test in enumerate(dictResultEleve):
        print(f'critere : {test["critere"]}')
        print(f'nom : {test["nom"]}')
        print(f'note : {test["note"]}')
        print(f'ponderation : {test["ponderation"]}')
        notes[test["critere"]] += test["note"]*(test["ponderation"]/100)
        if test["erreur"]:
            commentaires[test["critere"]] += (
                f'Vous avez echoué le test : {test["nom"][7:]}'
                f'Un exemple de vos erreurs est : {test["erreur"][0]}'
            )
    dicEquipe = {'équipe': GroupNb, 'score': ,
                 'commentaires': '<h4>Résultat critère 1</h4>'}


with open('./dictCritere.json') as templateJson:
    criteres = sorted(list(set([d['critere'] for d in dictResultEleve])))

for c in criteres:
    print(c)
    with open(f"./ResultatsSiteWeb_Critere{c}.json", "w") as SiteWebFile:
        JsonSiteWeb = json.load(SiteWebFile)

for i, json_eleve in enumerate(jsonEleves):
    with open('./ResultatsSiteWebC1.json') as SiteWebFile:
        JsonSiteWeb = json.load(SiteWebFile)
    if i == 2:
        # JsonSiteWeb.append(AddEleveResultSiteWeb(json_eleve))
        dictEquipe = AddEleveResultSiteWeb(json_eleve)
    JsonSiteWeb
