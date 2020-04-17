#!/bin/bash

sfdx force:org:display -u test --json > org.json

export token=$(cat org.json | python -c "import sys, json; print(json.load(sys.stdin)['result']['accessToken'])")
export instanceUrl=$(cat org.json | python -c "import sys, json; print(json.load(sys.stdin)['result']['instanceUrl'])")

echo $token
echo $instanceUrl

#"componentOption": "all" // Should be "all", "unmanaged" or "none"

curl --header 'Content-Type: application/json' --data '{
    "accessToken": "'$token'",
    "instanceUrl": "'$instanceUrl'",
    "componentOption": "unmanaged"}' https://packagebuilder.herokuapp.com/api/package/ > job.json

export idJob=$(cat job.json | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo $idJob

curl https://packagebuilder.herokuapp.com/api/package/status/$idJob/ > status.json
	
#	{"status": "Running", "success": false, "error": "", "done": false}
#	{"status": "Finished", "success": true, "error": "", "done": true}

export status=$(cat status.json | python -c "import sys, json; print(json.load(sys.stdin)['status'])")

while :
do
    if [ $status == 'Finished' ]; then
        echo $status
        break
    else 
        echo $status
        sleep 35
        curl https://packagebuilder.herokuapp.com/api/package/status/$idJob/ > status.json
        export status=$(cat status.json | python -c "import sys, json; print(json.load(sys.stdin)['status'])")
        #export success=$(cat status.json | python -c "import sys, json; print('true' if json.load(sys.stdin)['success'] else 'false')")
    fi
done

curl https://packagebuilder.herokuapp.com/api/package/$idJob > result.json

cat result.json | python -c "import sys, json; print(json.load(sys.stdin)['xml'])" > package.xml

rm result.json status.json job.json org.json