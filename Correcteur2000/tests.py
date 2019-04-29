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
            if self.team.noTeam == 15:
                print(classes_team)
                print(f"{self.team.dictNomenclature}")
                input()
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
            
    def test_2_prix(self):
        command = "prix"
        arg = "'goog', datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = 1168.685
        try:
            assert(getattr(self.marche, self.team.dictNomenclature[command])(
                str("goog"), datetime.date(2019, 3, 28)) == attendu)
            
        except AssertionError as e:
            res = False
            comments += f"<ul><li>La valeur retournée devrait être <code>{attendu}</code>.</li></ul>"
            print_failing(f'FAIL')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_3_deposer(self):
        command = "déposer"
        arg = "1000000.01"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = None
        try:
            assert(getattr(self.portefeuille, self.team.dictNomenclature[command])(
                1000000.01) == attendu)
            
        except AssertionError as e:
            print_warning(f'        WARNING')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_4_deposer(self):
        command = "déposer"
        arg = "2000000.02, datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = None
        try:
            assert(getattr(self.portefeuille, self.team.dictNomenclature[command])(
                2000000.02, datetime.date(2019, 3, 28)) == attendu)
            
        except AssertionError as e:
            print_warning(f'        WARNING')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_5_solde(self):
        command = "solde"
        arg = ""
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = 3000000.03
        try:
            assert(round(getattr(self.portefeuille, self.team.dictNomenclature[command])()) == round(attendu))
            
        except AssertionError as e:
            res = False
            test = getattr(self.portefeuille,
                           self.team.dictNomenclature[command])()
            print_warning(f"        Résultat attendu: {attendu}")
            print_failing(f"Résultat de l'équipe: {test}")
            comments += f"<ul><li>La valeur retournée devrait être <code>{attendu}</code>, vous retournez <code>{test}</code>. Prenez-vous en considération que l'argent déposé dans le passé restera dans le futur?</li></ul>"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_6_solde(self):
        command = "solde"
        arg = "datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = 2000000.02
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2019, 3, 28)) == attendu)
            
        except AssertionError as e:
            res = False
            test = getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2019, 3, 28))
            print_warning(f"        Résultat attendu: {attendu}")
            print_failing(f"Résultat de l'équipe: {test}")
            comments += f"<ul><li>La valeur retournée devrait être <code>{attendu}</code>, vous retournez <code>{test}</code>.</li></ul>"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_7_acheter(self):
        command = "acheter"
        arg = "'goog', 10"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = None
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])('goog', 10) == attendu)
            
        except AssertionError as e:
            print_warning(f'        WARNING')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_8_acheter(self):
        command = "acheter"
        arg = "'aapl', 10"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = None
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])('aapl', 10) == attendu)
            
        except AssertionError as e:
            print_warning(f'        WARNING')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_9_acheter(self):
        command = "acheter"
        arg = "'aapl', 10, datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = None
        try:
            assert(getattr(self.portefeuille, self.team.dictNomenclature[command])('aapl', 10, datetime.date(2019, 3, 28)) == attendu)
        except AssertionError as e:
            print_warning(f'        WARNING')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_10_vendre(self):
        command = "vendre"
        arg = "'goog', 5"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = None
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])('goog', 5) == attendu)
            
        except AssertionError as e:
            print_warning(f'        WARNING')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_11_vendre(self):
        command = "vendre"
        arg = "'aapl', 5, datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = None
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])('aapl', 5, datetime.date(2019, 3, 28)) == attendu)
            
        except AssertionError as e:
            print_warning(f'        WARNING')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_12_valeur_totale(self):
        command = "valeur_totale"
        arg = ""
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = 3000000.03
        try:
            assert(round(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])()) == round(attendu))
            
        except AssertionError as e:
            res = False
            test = getattr(self.portefeuille,
                           self.team.dictNomenclature[command])()
            print_warning(f"        Résultat attendu: {attendu}")
            print_failing(f"Résultat de l'équipe: {test}")
            comments += f"<ul><li>La valeur retournée devrait être <code>{attendu}</code>, vous retournez <code>{test}</code>.</li></ul>"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_13_valeur_totale(self):
        command = "valeur_totale"
        arg = "datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = 2000000.02
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2019, 3, 28)) == attendu)
            
        except AssertionError as e:
            res = False
            test = getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2019, 3, 28))
            print_warning(f"        Résultat attendu: {attendu}")
            print_failing(f"Résultat de l'équipe: {test}")
            comments += f"<ul><li>La valeur retournée devrait être <code>{attendu}</code>, vous retournez <code>{test}</code>.</li></ul>"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_14_valeur_des_titres(self):
        command = "valeur_des_titres"
        arg = "['goog']"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = 6360.9
        try:
            assert(round(getattr(self.portefeuille,
                                 self.team.dictNomenclature[command])(['aapl', 'goog'])) == round(attendu))
            
        except AssertionError as e:
            res = False
            test = getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(['aapl', 'goog'])
            print_warning(f"        Résultat attendu: {attendu}")
            print_failing(f"Résultat de l'équipe: {test}")
            comments += f"<ul><li>La valeur retournée devrait être <code>{attendu}</code>, vous retournez <code>{test}</code>.</li></ul>"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_15_valeur_des_titres(self):
        command = "valeur_des_titres"
        arg = "['aapl', 'goog']"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = 9345.769
        try:
            assert(round(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(['aapl', 'goog'])) == round(attendu))
            
        except AssertionError as e:
            res = False
            test = getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(['aapl', 'goog'])
            print_warning(f"        Résultat attendu: {attendu}")
            print_failing(f"Résultat de l'équipe: {test}")
            comments += f"<ul><li>La valeur retournée devrait être <code>{attendu}</code>, vous retournez <code>{test}</code>. Prenez-vous en considération que la valeur de titre acheté dans le passé restera dans le futur?</li></ul>"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)
#1963.3339
    def test_16_valeur_des_titres(self):
        command = "valeur_des_titres"
        arg = "['aapl'], datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = 941.869
        try:
            assert(round(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(['aapl'], datetime.date(2019, 3, 28))) == round(attendu))
            
        except AssertionError as e:
            res = False
            test = getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(['aapl'], datetime.date(2019, 3, 28))
            print_warning(f"        Résultat attendu: {attendu}")
            print_failing(f"Résultat de l'équipe: {test}")
            comments += f"<ul><li>La valeur retournée devrait être <code>{attendu}</code>, vous retournez <code>{test}</code>.</li></ul>"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_17_titres(self):
        command = "titres"
        arg = ""
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = {'goog': 5, 'aapl': 15}
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])() == attendu)
            
        except AssertionError as e:
            res = False
            test = getattr(self.portefeuille,
                           self.team.dictNomenclature[command])()
            print_warning(f"        Résultat attendu: {attendu}")
            print_failing(f"Résultat de l'équipe: {test}")
            comments += f"<ul><li>La valeur retournée devrait être <code>{attendu}</code>, vous retournez <code>{test}</code>. Avez-vous considéré que les actions achetés dans le passé reste dans le futur?</li></ul>"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur  <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_18_titres(self):
        command = "titres"
        arg = "datetime.date(2019, 3, 28)"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = {'aapl': 5}
        try:
            assert(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2019, 3, 28))['aapl'] == 5)
            
        except AssertionError as e:
            res = False
            test = getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2019, 3, 28))
            print_warning(f"        Résultat attendu: {attendu}")
            print_failing(f"Résultat de l'équipe: {test}")
            comments += f"<ul><li>La valeur retournée devrait être <code>{attendu}</code>, vous retournez <code>{test}</code>.</li></ul>"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_19_valeur_projetee(self):
        command = "valeur_projetée"
        arg = "datetime.date(2021, 3, 28), 5.5"
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = 3000727.488
        try:
            assert(round(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2021, 3, 28), 5.5)) == round(attendu))
            
        except AssertionError as e:
            res = False
            test = getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2021, 3, 28))
            print_warning(f"        Résultat attendu: {attendu}")
            print_failing(f"Résultat de l'équipe: {test}")
            comments += f"<ul><li>La valeur retournée devrait être <code>{attendu}</code>, vous retournez <code>{test}</code>.</li></ul>"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def test_20_valeur_projetee(self):
        command = "valeur_projetée"
        arg = """datetime.date(2021, 3, 28), {"goog": 5.0}"""
        print_command(f"{command}", f"{arg}")
        res = True
        comments = f"<li>{command}({arg})</li>"
        attendu = 3000495.832
        try:
            assert(round(getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2021, 3, 28), {"goog": 5.0})) == round(attendu))
            
        except AssertionError as e:
            res = False
            test = getattr(self.portefeuille,
                           self.team.dictNomenclature[command])(datetime.date(2021, 3, 28))
            print_warning(f"        Résultat attendu: {attendu}")
            print_failing(f"Résultat de l'équipe: {test}")
            comments += f"<ul><li>La valeur retournée devrait être <code>{attendu}</code>, vous retournez <code>{test}</code>.</li></ul>"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            res = False
            comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> à la ligne {exc_tb.tb_lineno} du fichier {fname}.</li></ul>"
            print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def erreur_0_1_depot(self):
        command = "déposer"
        arg = """1"""
        print_command(f"{command}", f"{arg}")
        comments = f"<li>{command}({arg})</li>"
        try:
            getattr(self.portefeuille, self.team.dictNomenclature[command])(1)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print_failing(f"{e.__class__.__name__}: {exc_obj}")

    def erreur_0_liquid_acheter(self):
        command = "acheter"
        arg = """'goog', 100"""
        print_command(f"{command}", f"{arg}")
        res = False
        comments = f"<li>{command}({arg})</li>"
        attendu = "LiquiditéInsuffisante"
        try:
            getattr(self.portefeuille, self.team.dictNomenclature[command])('goog', 100)
            comments += f"<ul><li>Votre programme ne retourne aucune erreur alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
            print_failing(f"FAIL")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if e.__class__.__name__ == self.team.dictNomenclature[attendu]:
                res = True
            else:
                res = False
                comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
                print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def erreur_1_date_prix(self):
        command = "prix"
        arg = """'goog', datetime.date(2022, 3, 28)"""
        print_command(f"{command}", f"{arg}")
        res = False
        comments = f"<li>{command}({arg})</li>"
        attendu = "ErreurDate"
        try:
            getattr(self.marche, self.team.dictNomenclature[command])('goog', datetime.date(2022, 3, 28))
            comments += f"<ul><li>Votre programme ne retourne aucune erreur alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
            print_failing(f"FAIL")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if e.__class__.__name__ == self.team.dictNomenclature[attendu]:
                res = True
            else:
                res = False
                comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
                print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def erreur_2_date_déposer(self):
        command = "déposer"
        arg = """20000.02, datetime.date(2022, 3, 28)"""
        print_command(f"{command}", f"{arg}")
        res = False
        comments = f"<li>{command}({arg})</li>"
        attendu = "ErreurDate"
        try:
            getattr(self.portefeuille, self.team.dictNomenclature[command])(
                'goog', datetime.date(2022, 3, 28))
            comments += f"<ul><li>Votre programme ne retourne aucune erreur alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
            print_failing(f"FAIL")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if e.__class__.__name__ == self.team.dictNomenclature[attendu]:
                res = True
            else:
                res = False
                comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
                print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def erreur_3_date_solde(self):
        command = "solde"
        arg = """datetime.date(2022, 3, 28)"""
        print_command(f"{command}", f"{arg}")
        res = False
        comments = f"<li>{command}({arg})</li>"
        attendu = "ErreurDate"
        try:
            getattr(self.portefeuille, self.team.dictNomenclature[command])(datetime.date(2022, 3, 28))
            comments += f"<ul><li>Votre programme ne retourne aucune erreur alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
            print_failing(f"FAIL")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if e.__class__.__name__ == self.team.dictNomenclature[attendu]:
                res = True
            else:
                res = False
                comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
                print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def erreur_4_date_acheter(self):
        command = "acheter"
        arg = """'goog', 1, datetime.date(2022, 3, 28)"""
        print_command(f"{command}", f"{arg}")
        res = False
        comments = f"<li>{command}({arg})</li>"
        attendu = "ErreurDate"
        try:
            getattr(self.portefeuille, self.team.dictNomenclature[command])(
                'goog', 1, datetime.date(2022, 3, 28))
            comments += f"<ul><li>Votre programme ne retourne aucune erreur alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
            print_failing(f"FAIL")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if e.__class__.__name__ == self.team.dictNomenclature[attendu]:
                res = True
            else:
                res = False
                comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
                print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def erreur_4_1_depot(self):
        command = "déposer"
        arg = """1000000"""
        print_command(f"{command}", f"{arg}")
        comments = f"<li>{command}({arg})</li>"
        try:
            getattr(self.portefeuille, self.team.dictNomenclature[command])(1000000)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print_failing(f"{e.__class__.__name__}: {exc_obj}")

    def erreur_4_2_achat(self):
        command = "acheter"
        arg = """'goog', 2"""
        print_command(f"{command}", f"{arg}")
        comments = f"<li>{command}({arg})</li>"
        try:
            getattr(self.portefeuille,
                    self.team.dictNomenclature[command])('goog', 2)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print_failing(f"{e.__class__.__name__}: {exc_obj}")

    def erreur_5_date_vendre(self):
        command = "vendre"
        arg = """'goog', 1, datetime.date(2022, 3, 28)"""
        print_command(f"{command}", f"{arg}")
        res = False
        comments = f"<li>{command}({arg})</li>"
        attendu = "ErreurDate"
        try:
            getattr(self.portefeuille, self.team.dictNomenclature[command])(
                'goog', 1, datetime.date(2022, 3, 28))
            comments += f"<ul><li>Votre programme ne retourne aucune erreur alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
            print_failing(f"FAIL")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if e.__class__.__name__ == self.team.dictNomenclature[attendu]:
                res = True
            else:
                res = False
                comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
                print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def erreur_6_date_valeur_totale(self):
        command = "valeur_totale"
        arg = """datetime.date(2022, 3, 28)"""
        print_command(f"{command}", f"{arg}")
        res = False
        comments = f"<li>{command}({arg})</li>"
        attendu = "ErreurDate"
        try:
            getattr(self.portefeuille, self.team.dictNomenclature[command])(datetime.date(2022, 3, 28))
            comments += f"<ul><li>Votre programme ne retourne aucune erreur alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
            print_failing(f"FAIL")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if e.__class__.__name__ == self.team.dictNomenclature[attendu]:
                res = True
            else:
                res = False
                comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
                print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def erreur_7_date_valeur_titres(self):
        command = "valeur_des_titres"
        arg = """["goog"], datetime.date(2022, 3, 28)"""
        print_command(f"{command}", f"{arg}")
        res = False
        comments = f"<li>{command}({arg})</li>"
        attendu = "ErreurDate"
        try:
            getattr(self.portefeuille, self.team.dictNomenclature[command])(["goog"], datetime.date(2022, 3, 28))
            comments += f"<ul><li>Votre programme ne retourne aucune erreur alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
            print_failing(f"FAIL")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if e.__class__.__name__ == self.team.dictNomenclature[attendu]:
                res = True
            else:
                res = False
                comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
                print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def erreur_8_date_titres(self):
        command = "titres"
        arg = """datetime.date(2022, 3, 28)"""
        print_command(f"{command}", f"{arg}")
        res = False
        comments = f"<li>{command}({arg})</li>"
        attendu = "ErreurDate"
        try:
            getattr(self.portefeuille, self.team.dictNomenclature[command])(datetime.date(2022, 3, 28))
            comments += f"<ul><li>Votre programme ne retourne aucune erreur alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
            print_failing(f"FAIL")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if e.__class__.__name__ == self.team.dictNomenclature[attendu]:
                res = True
            else:
                res = False
                comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
                print_failing(f"{e.__class__.__name__}: {exc_obj}")
        finally:
            return (res, comments)

    def erreur_9_quantite_vendre(self):
        command = "vendre"
        arg = """'goog', 10000"""
        print_command(f"{command}", f"{arg}")
        res = False
        comments = f"<li>{command}({arg})</li>"
        attendu = "ErreurQuantité"
        try:
            getattr(self.portefeuille, self.team.dictNomenclature[command])(
                'goog', 10000)
            comments += f"<ul><li>Votre programme ne retourne aucune erreur alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
            print_failing(f"FAIL")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if e.__class__.__name__ == self.team.dictNomenclature[attendu]:
                res = True
            else:
                res = False
                comments += f"<ul><li>Votre programme retourne l'erreur <code>{e.__class__.__name__}: {exc_obj}</code> alors que nous aurions du avoir une erreur de type <code>{attendu}</code>.</li></ul>"
                print_failing(f"{e.__class__.__name__}: {exc_obj}")
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

