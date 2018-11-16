cd ../unbundled
ls | while read line ;
do cd "$line"
num=$(echo $line| cut -d'-' -f 2)
echo "Doing $line"
python ../../ScriptCorrection/CorrectionAuto.py ../../ScriptCorrection/Corrige.py ./*.py &>Resultat_$num.txt
echo "Done $line"
echo ""
cd ..;
done
echo "Correction terminée ! Veuillez lancer moulinetteMakeJson pour créer les fichiers json."
