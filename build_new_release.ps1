#This script is for closing the release flow in git repo
#-release is a name of the tag related to relese
$release = Read-Host -Prompt "Input the name of the tag release: " 

$location = Get-Location
Set-Location -path 'C:\Users\Emiliano Fama\Documents\Repositorios\bitbucket\communities-accelerator'

Write-Output "Builde Release"
git checkout development
git pull origin development
git checkout release
git pull origin release
git merge development --no-commit
git push origin release
git checkout master
git pull origin master
git merge release --no-commit
git push origin master
git tag $release
git push origin $release
git checkout HOTFIX
git pull origin HOTFIX
git merge master --no-commit
git push origin HOTFIX

Set-Location -Path $location