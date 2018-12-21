cd ..
mkdir unbundled
cd A18-P3-bundles/
ls | grep .hg | while read line ;
do mkdir ../unbundled/"$line"/ ;
cp "$line" ../unbundled/"$line"/ ;
cd ../unbundled/"$line"/ ;
echo "Doing $line"
hg init ;
hg unbundle "$line" ;
hg update ;
echo "Done $line"
cd ../../A18-P3-bundles;
done
echo "Unbundle terminé ! Veuillez lancer moulinetteCorrection pour lancer la correction (peut être long...)."
