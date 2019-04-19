import sys
import traceback
sys.path.insert(0,"./H19-P2/unbundled/bundle-028-13/")
module = "marche_boursier"
try:
    __import__(module)
except ModuleNotFoundError:
    print(f"No module {module} for team {team.noTeam}")
except Exception:
    print(f"Module {module} importé mais non fonctionel team : {team.noTeam}")
    traceback.print_exc()
finally:
    print("Team Suivante")
