#! /usr/bin/env python
import argparse
import glob
import json
import os
import re
import shutil
import zipfile
from math import ceil
from subprocess import PIPE, Popen, TimeoutExpired
from SuperCorrecteur2000 import SuperCorrecteur2000
from utils import unbundle, unzip

path_to_folder_or_zip = './A18-P2-bundles.zip'
# ########################################
# Argparse pour tout les éléments voulus #
# ########################################
TP = path_to_folder_or_zip[4:6]
if not os.path.exist(f"./{TP}"):
    os.makedirs(f"./{TP}")

# Avec l'option unzip
if zipfile.is_zipfile(path_to_folder_or_zip):
    unzip(path_to_folder_or_zip,
          f"./{TP+'/'+path_to_folder_or_zip[-4:]}")

# Avec l'option unbundle
if (os.path.isfile(os.listdir(path_to_folder_or_zip)[0]) and
        os.listdir(path_to_folder_or_zip)[0][-3:] == '.hg'):
    if not os.path.exist(f"./{TP}/Unbundled"):
        os.makedirs(f"./{TP}/Unbundled")
    unbundle(path_to_folder_or_zip, f"./{TP}/Unbundled")

# Avec l'option correction (dosssier déjà unbundlé)
if (os.path.isdir(os.listdir(path_to_folder_or_zip)[0])):
    SuperCorrecteur2000(path_to_json_correction, path_to_folder_or_zip,
                        nom_fichier_main)
    # Différentes ooptions du argparse :
    SuperCorrecteur2000.cleanResultatsEleves
    SuperCorrecteur2000.cleanResultatsSiteWeb
    SuperCorrecteur2000.cleanToutResultats
    SuperCorrecteur2000.getAllGroupsNumber
    SuperCorrecteur2000.getIncorrectGroupsNumber
    SuperCorrecteur2000.getIncorrectGroupsPath
    SuperCorrecteur2000.getCorrectGroupsNumber
    SuperCorrecteur2000.getCorrectGroupsPath
    SuperCorrecteur2000.getNumberSubmissions
    SuperCorrecteur2000.createResultatsSiteWeb
    SuperCorrecteur2000.critereToJson
    SuperCorrecteur2000.correctBadBundles
    SuperCorrecteur2000.correctGoodBundles
    SuperCorrecteur2000.correctAll
