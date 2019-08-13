
#git diff --name-status master >> diff.txt
input="./diff.txt"
mkdir deploy
destiny="$PWD/deploy/"
#cp -p ./src/package.xml ./deploy/package.xml
while read line
do
  if test ${line:0:1} != 'D'
    then
    origin="${line:6}"
    cd src
    cp --parents $origin $destiny
    cd ..
  #else
    #echo "Es para borrar"
  fi
done < "$input"
#rm -rf diff.txt