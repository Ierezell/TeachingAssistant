# TP à unbundler
TP=TP1/
# Nom du dossier ou se trouve les bundles ex : H19-P1-bundles format:`Session Année-no du TP-bundles`
BUNDLE=H19-P1-bundles/
cd $TP
mkdir unbundled
cd $BUNDLE
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
