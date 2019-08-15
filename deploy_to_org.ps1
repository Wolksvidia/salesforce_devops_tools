#Deploy metatdata from git repo.
#-org parameter is org alias in CLI.
#-branch is name of the git branch to deploy.
#-code is the folder that contain metadata in the repo.

Param([string] $org="CMSDev", [string] $branch="development", [string] $code="src")

$location = Get-Location
Set-Location -path 'C:\Users\Emiliano Fama\Documents\Repositorios\bitbucket\communities-accelerator'

Write-Output "Change branch"
git checkout $branch
Write-Output "Pull changes from origin"
git pull origin $branch
Write-Output "Deploy metadata"
sfdx force:mdapi:deploy -d $code -u $org -w 10

Set-Location -Path $location