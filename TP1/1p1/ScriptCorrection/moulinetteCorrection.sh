ProjetPatern="[P|p][R|r][O|o][J|j][E|e][T|t].?1\.py"
cd ../unbundled
FichierTrouve=0
ls | while read folder ;
    do cd "$folder"
    num=$(echo $folder| cut -d'-' -f 2)
    echo "Doing $folder"
    FichierTrouve=0
    ls |{
        while read file;
        do
        if [[ $file =~ $ProjetPatern ]]; then
            echo "Correction bundle $file"
            FichierTrouve=$((FichierTrouve + 1))
            python ../../ScriptCorrection/CorrectionAuto2.py ../../ScriptCorrection/Corrige.py $file &>Resultat_$num.txt
        fi
    done
    if [ $FichierTrouve -eq 0 ];then
        echo "La recherche d'un fichier Projet1.py dans le dossier $folder à échoué, la correction n'a pas pu être faite" &> Resultat_$num.txt
    fi
    }
echo "Done $folder"
echo ""
cd ..;
done

echo "Correction terminée ! Veuillez lancer moulinetteMakeJson pour créer le fichiers de résultats."

# TODO Check si file
