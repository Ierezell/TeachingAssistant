cd ../unbundled
ls | while read line ;
do cd "$line"
num=$(echo $line| cut -d'-' -f 2)
echo "Doing $line"
python ../../ScriptCorrection/CorrectionAuto.py ../../ScriptCorrection/Corrige.py ./*.py >Res_Detail_$num.txt 2>Resume_$num.txt
echo "Done $line"
cd ..;
done
echo "Correction terminée ! Veuillez lancer moulinetteMakeJson pour créer les fichiers json."
