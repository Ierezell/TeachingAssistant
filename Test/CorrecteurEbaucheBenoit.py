"""
Ébauche de classe pour correcteur automatisé de ligne de commande
"""

from typing import Dict, List


"""
Classe SuperCorrecteur, contient les équipes
"""
@dataclass(order=True)
class SuperCorrecteur:
    equipe_dict: Dict[Equipe] = {}

    def add_equipes(self, *equipes: Equipe):
        return 0

    def unbundled(self, path):
        return 0

    def corriger_critère(self, no_critere: int):
        return 0

    def corriger_projet(self, no_projet: int):
        return 0

    def corriger_equipe(self, no_equipe: int):
        return 0


"""
Classe Equipe, contient tous les projets de cette équipe
"""
@dataclass(order=True)
class Equipe:
    no_equipe: int
    projet_dict: dict = {}
    
    def resume_note_projet(self, no_projet: int) -> str:
        return self.projet_list[no_projet].resume_note()
    
    def detaille_note_projet(self, no_projet: int) -> str:
        return self.projet_list[no_projet].detaille_note()

    def resume_note(self):
        for i in range(1, self.projet_dict.len()):
            self.resume_note_projet(i)

    def detaille_note(self):
        for i in range(1, self.projet_dict.len()):
            self.detaille_note_projet(i)



"""
Classe Projet, contient les énoncés et les critères
"""
@dataclass(order=True)
class Projet:
    no_projet: int
    nom_fichier: str # Ex : projet.py
    critere_list: list = []
    enoncer_list: list = []


"""
Classe Critere, contient les tests, la pondération d'un critère, son descriptif
"""
@dataclass(order=True)
class Critere:
    no_critere: int
    description: str
    ponderation: float
    tests_list: list = []

    def add_tests(self, *tests: Test):
        self.test_list.append(list(tests))

    def show_tests(self):
        return ""


"""
Classe Test, contient les commandes à tester, la pondération du test sur le critère, nom et descriptions
"""
@dataclass(order=True)
class Test(Critere):
    nom: str

    @propriety
    def commandes_list(self):
        return self.tests_list

    def add_commandes(self, commandes: List[Commande]):
        self.commandes_list.append(commandes)
    

"""
Classe Commande, une commandes à tester, si on s'Attend à une erreur ou a un succes, les variantes attendu de ce succès ou échec
"""
@dataclass(order=True)
class Commande:
    commande: str
    is_erreur: bool
    attendus_list: List[str] = []
