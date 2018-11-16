cd ..
if [ -d "Resultats" ]; then
    rm -rf Resultats
    mkdir Resultats
    find -iname "ResultatC3*.txt" -type f -exec cp {} ./Resultats \;
else
    mkdir Resultats
    find -iname "ResultatC3*.txt" -type f -exec cp {} ./Resultats \;
fi
echo "Copie terminée !"
