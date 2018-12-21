# Fichiers de corrections de Travaux pratiques en python. 
Pour réaliser la **correction :**

Cloner le répertoire :
```
$ git clone https://github.com/Ierezell/TeachingAssistant
```
Ou télécharger le [**FichierZip**](https://github.com/Ierezell/TeachingAssistant/archive/master.zip) et unziper le. 

Ensuite, copier le répertoire **ScriptCorrection** dans le dossier avec tout les bundles mercurials. 
```
$ cp ScriptCorrection /Chemin/Vers/Le/Dossier/Des/Bundles
```
Deplacer vous dans ce dossier 
```
$ cd /Chemin/Vers/Le/Dossier/Des/Bundles/ScriptCorrection
```
Puis lancer (de préférence dans un terminal pour voir l'avancement)
```
$ ./moulinetteUnbundle.sh
```
Va créer les dossiers pour chaque étudiants. 
```
$ ./moulinetteCorrection.sh
```
Va corriger les Tps (Pour d'autres Tps, simplement changer les tests dans params.txt et le corrigé Corrige.py)
Cela va aussi créer Resume_N°Groupe.txt (résumé de correction) et Res_Detail_N°Groupe.txt (Détail précis de la correction)
Puis
```
$ ./moulinetteMakeJson.sh
```
Crée les fichiers identiques en Json pour les exporter sur le site. 
Enfin
```
$ ./moulinetteGroupJson.sh
```
Regroupe tout les résultats (.json) des élèves dans un dossier resultats pour un upload plus simple. 
