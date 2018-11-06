cd ..
mkdir unbundled
ls | grep .hg | while read line ;
do mkdir unbundled/"$line" ;
cp "$line" unbundled/"$line" ;
cd unbundled/"$line" ;
echo "Doing $line"
hg init ;
hg unbundle "$line" ;
hg update ;
echo "Doing $line"
cd ../.. ;
done
echo "Unbundle terminé ! Veuillez lancer moulinetteCorrection pour lancer la correction (peut être long...)."
