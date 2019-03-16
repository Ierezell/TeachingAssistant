mkdir unbundled
ls | grep .hg | while read line ;
do mkdir ../unbundled/"$line"/ ;
cp "$line" ../unbundled/"$line"/ ;
cd ../unbundled/"$line"/ ;
echo "Doing $line"
hg init ;
hg unbundle "$line" ;
hg update ;
echo "Done $line"
cd ../../$BUNDLE;
done
echo "Unbundle terminé ! Veuillez lancer Correction.py pour lancer la correction (peut être long...)."
