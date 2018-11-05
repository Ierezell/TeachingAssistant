mkdir unbundled
ls | grep .hg | while read line ;
do mkdir unbundled/"$line" ;
cp "$line" unbundled/"$line" ;
cd unbundled/"$line" ;
hg init ;
hg unbundle "$line" ;
hg update ;
python ../../Correction.py ./projet1.py > ./ResultatsTests_"$line".txt
cd ../.. ;
done
