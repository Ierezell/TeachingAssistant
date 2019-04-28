import sys
import importlib
import traceback
import os
import datetime


class Tests:
    def __init__(self, team, modules, classes):
        # Création de l'objet de test qui charge les modules et effectue les
        # tests. (modules et tests doivent etre dans le meme fichier....)
        # TREES IMPORTANT DAPELLER LA FONCTION CLEANUP A LA FIN !
        self.classes = classes
        self.team = team
        self.modules = tuple(team.dictNomenclature[module] for module in modules)
        self.init_modules = sys.modules.keys()
        os.chdir(team.pathTeam)
        sys.path.insert(0, os.getcwd())
        self.modules_to_remove = []
        self.loaded_modules = list([None]*len(self.modules))
        self.equipeOk = True
        # print(team.noTeam)
        missing_module_name = None
        missing_module = None
        for i, module in enumerate(self.modules):
            try:
                self.loaded_modules[i] = importlib.import_module(module)
                self.loaded_modules[i] = importlib.reload(self.loaded_modules[i])
            except ModuleNotFoundError:
                #print(f"No module {module} for team {team.noTeam}")
                self.equipeOk = False
            except ImportError:
                missing_module_name = traceback.format_exc().split('\n')[-2].split()[6][1:-1]
                if missing_module_name == module:
                    #print("Import circulaire !")
                    self.equipeOk = False
                else:
                    self.modules_to_remove.append(missing_module_name)
                    missing_module = importlib.import_module(missing_module_name)
                    missing_module = importlib.reload(missing_module)
                    self.loaded_modules[i] = importlib.import_module(module)
                    self.loaded_modules[i] = importlib.reload(self.loaded_modules[i])
            except Exception as e:
                print(e)
                self.equipeOk = False
        # A PARTIE DICI LES MODULES SONT CHARGÉ DANS loaded_modules
        # OU ALORS LEQUIPE A UN PROBLEME ET ON NE PEUT PAS CHARGER LEURS
        # MODULES AUTOMATIQUEMENT

    # CLEANUP TRES IMPORTANT, IL DOIT ETRE APELLE DANS LE CORRECTIONEUR

    def cleanUp(self):
        for module in self.modules_to_remove:
            del sys.modules[module]
        for module in self.modules:
            if module in sys.modules:
                del sys.modules[module]
        for modulilou in sys.modules.keys():
            if modulilou not in self.init_modules:
                del(sys.modules[modulilou])
        sys.path.remove(os.getcwd())
        os.chdir('../../../')

    def loadClassObject(self):
        if self.equipeOk:
            classes_team = []
            # ICI ON CHERCHE LES CLASSES DES ELEVES EN FONCTION DE CELLES QUON
            # VEUT DEPUIS LES STRING DONNEES DANS SUPERCORRECTEUR ET PASSEE
            # DANS TA MOULINETTE DE RECHERCHE DE NOMS
            for i, mod in enumerate(self.loaded_modules):
                for cl in self.classes[i]:
                    classes_team.append(getattr(mod, self.team.dictNomenclature[cl]))
            try:
                self.marche = classes_team[0]()
            except Exception as e:
                print(e)
            try:
                # self.portefeuille = classes_team[1]()
                # Ou bien
                self.portefeuille = classes_team[1](self.marche)
                # Pour initialiser le portefeuille avec un marché

            except Exception as e:
                print(e)
##############################################################################
##############################################################################
#                          DEFINE ALL THE TESTS BELLOW                       #
##############################################################################
##############################################################################

    def test_vendre_GOOG_2018_5_8(self):
        #print("JE FAIS LE TEST DU MARHCE OUIIIIIIIIII")
        # LOAD CLASS OBJECT PERMET DE RECHARGER A CHAQUE FOIS UN NOUVEAU MARCHE
        self.loadClassObject()
        try:
            # SELF.MARCHE et SELF.PORTEFEUILLE SONT CHARGE A CHAQUE FOIS
            # Y'A PLUS QUA DEFINIR LES TESTS QUON VEUT

            # GETATTR PERMET DE PRENDRE LA FOCNTION PRIX MAIS QUI A PEUT ETRE
            # UN NOM DIFFERENT CHEZ LETUDIANT
            print(type(getattr(self.marche,
                               self.team.dictNomenclature["prix"])
                       (str("GOOG")))
                  )
            # getattr(marche.prix)(args)
            # REVIENT A FAIRE marche.prix(args)
            #print("JAI PRINT LE TEST DU MARHCE WAAAAAAAAAAAAAAAA")
        # traceback.format_exc()
        except Exception as e:
            return print(e)
