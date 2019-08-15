#This script run all test ind org and print report.
#-org parameter is the alias for the org in the CLI.

Param([string] $org="CMSDev")

$location = Get-Location
New-Item -Path $location -Name "test-reports" -ItemType "directory"

sfdx force:apex:test:run -l RunAllTestsInOrg -r junit -d test-reports --verbose -u $org -w 10

Remove-Item -Path "$($location)\test-reports" -Recurse