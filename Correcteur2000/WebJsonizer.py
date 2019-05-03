import json


class WebJsonizer:
    def __init__(self):
        pass

    def makeRapport(self, team):
        for critere in team.sortie.values():
            noteCritere = 0
            for nomTest in critere.keys():
                noteTest = 0
                for args in critere[nomTest]["arguments"]:
                    if args["erreur"]:
                        coms.append(f"<p>{args['comErreur']}</p>")
                    #
                    #
                    # TODO faire la logique de l'ajout des commentaires
                    #
                    #
                coms = f"Test : {nomTest} [{noteTest}/100]" + coms
            coms = f"<p><h2>Évaluation du critère {critere} [{noteCritere}/100]</h2></p>" + coms
        team.rapport = dictSite

    def jsonizeResults(self, listTeam):
        jsonSite = []
        for team in listTeam:
            rapport = team.rapport
            jsonSite.append(rapport)

        with open(f'whatever.json', 'w') as outfile:
            json.dump(jsonSite, outfile, ensure_ascii=False)
