import sys
import importlib
import traceback
import os
import datetime
from Log import *


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
<<<<<<< HEAD
            
    def test_1_prix(self):
        command = "prix"
        arg = "'GOOG'"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = 1272.18
        try:
            assert(getattr(self.marche, self.team.dictNomenclature[command])(
                str("GOOG")) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments + \
                f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_2_prix(self):
        command = "prix"
        arg = "'GOOG', datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = 1168.685
        try:
            assert(getattr(self.marche, self.team.dictNomenclature[command])(
                str("GOOG"), datetime.date(2019, 3, 28)) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_3_deposer(self):
        command = "déposer"
        arg = "10000.01"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = None
        try:
            assert(getattr(self.portefeuille, self.team.dictNomenclature[command])(
                10000.01) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_4_deposer(self):
        command = "déposer"
        arg = "20000.02, datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = None
        try:
            assert(getattr(self.portefeuille, self.team.dictNomenclature[command])(
                20000.02, datetime.date(2019, 3, 28)) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_5_solde(self):
        command = "solde"
        arg = ""
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = 10000.01
        try:
            assert(getattr(self.portefeuille, self.team.dictNomenclature[command])() == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_6_solde(self):
        command = "solde"
        arg = "datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = 20000.02
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2019, 3, 28)) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_6_acheter(self):
        command = "acheter"
        arg = "'GOOG', 10"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = None
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])('GOOG', 10) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_7_acheter(self):
        command = "acheter"
        arg = "'AAPL', 10"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = None
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])('AAPL', 10) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_8_acheter(self):
        command = "acheter"
        arg = "'AAPL', 10, datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = None
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])('AAPL', 10, datetime.date(2019, 3, 28)) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_9_vendre(self):
        command = "vendre"
        arg = "'GOOG', 5"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = None
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])('GOOG', 5) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_10_vendre(self):
        command = "vendre"
        arg = "'AAPL', 5, datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = None
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])('AAPL', 5, datetime.date(2019, 3, 28)) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_11_valeur_totale(self):
        command = "valeur_totale"
        arg = ""
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = 8423.9
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])() == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_12_valeur_totale(self):
        command = "valeur_totale"
        arg = "datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = 1883.738
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2019, 3, 28)) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_14_valeur_des_titres(self):
        command = "valeur_des_titres"
        arg = "['AAPL', 'GOOG']"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = 1883.738
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(['AAPL', 'GOOG']) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_15_valeur_des_titres(self):
        command = "valeur_des_titres"
        arg = "['AAPL'], datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = 1883.738
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(['AAPL'], datetime.date(2019, 3, 28)) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_16_titres(self):
        command = "titres"
        arg = ""
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = {'goog': 5, 'aapl': 10}
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])() == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

    def test_17_titres(self):
        command = "titres"
        arg = "datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = ""
        attendu = {'aapl': 5}
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2019, 3, 28)) == attendu)
            comments += ""
        except AssertionError as e:
            res = False
            comments += f"<li><code>{command}({arg})</code> la retourner devrait être <code>{attendu}</code>.</li>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<li><code>{command}({arg})</code> retourne une erreur de type <code>{e.__class__.__name__}</code> à la ligne {exc_tb.tb_lineno} du fichier fname.</li>"
            print_failing(f"Error: {e.__class__.__name__}")
        finally:
            return (res, comments)

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
=======
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
>>>>>>> dc5a23b300a4d62b038b897b5a87ec35a9a25cbf
