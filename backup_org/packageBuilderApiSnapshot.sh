#!/bin/bash

#===========================================================
#   Script for take a snapsho of a Salesforce Org
#===========================================================
#   It's necessary to set the variables below 
#   location= Full path git repo
#   branch= brach of git repo to perform snapshot
#   org= Alias of Salesforce org in cli
#===========================================================

org=test
location=
branch=

#Package builder Api Urls
apijob="https://packagebuilder.herokuapp.com/api/package/"
apistatus="https://packagebuilder.herokuapp.com/api/package/status/"

#Set location of the git project
cd $location
git checkout $branch

#take token and instanceurl from cli
sfdx force:org:display -u $org --json > org.json

token=$(cat org.json | python -c "import sys, json; print(json.load(sys.stdin)['result']['accessToken'])")
instanceUrl=$(cat org.json | python -c "import sys, json; print(json.load(sys.stdin)['result']['instanceUrl'])")

echo $token
echo $instanceUrl

#Request job to api
#"componentOption"// Should be "all", "unmanaged" or "none"
curl --header 'Content-Type: application/json' --data '{
    "accessToken": "'$token'",
    "instanceUrl": "'$instanceUrl'",
    "componentOption": "unmanaged"}' $apijob > job.json

idJob=$(cat job.json | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo $idJob

#Request status
#Responses
#	{"status": "Running", "success": false, "error": "", "done": false}
#	{"status": "Finished", "success": true, "error": "", "done": true}
sleep 60
curl $apistatus$idJob/ > status.json

status=$(cat status.json | python -c "import sys, json; print(json.load(sys.stdin)['status'])")
success=$(cat status.json | python -c "import sys, json; print('true' if json.load(sys.stdin)['success'] else 'false')")

while :
do
    if [ $status == 'Finished' ]; then
        echo $status
        break
    else 
        echo $status
        sleep 60
        curl $apistatus$idJob/ > status.json
        status=$(cat status.json | python -c "import sys, json; print(json.load(sys.stdin)['status'])")
        success=$(cat status.json | python -c "import sys, json; print('true' if json.load(sys.stdin)['success'] else 'false')")
    fi
done

if [ "$success" == "false" ]; then
    echo "ERROR: The process has finished with erros, take some minutes and re-run the script."
    exit 1
fi

#Request results
curl $apijob$idJob > result.json

cat result.json | python -c "import sys, json; print(json.load(sys.stdin)['xml'])" > package.xml

rm result.json status.json job.json org.json

#Retrieve metadata
sfdx force:mdapi:retrieve -r . -u $org -k package.xml

#Extract metadata 
#https://www.hostingmanual.net/zipping-unzipping-files-unix/
unzip -a -u unpackaged.zip
cp -pav unpackaged/. src
rm -rf unpackaged unpackaged.zip

#Commit new metadata
date=$(date '+snapshot-%d-%m-%Y')
git add .
git commit -m $date
git push origin $branch