#Deploy metatdata differnce between development branch and master. The repo is cloned in place for this.
#-org parameter is org alias in CLI.
#-branch is name of the git branch to deploy.
#-code is the folder that contain metadata in the repo.

Param([string] $org="efadev", [string] $branch="development", [string] $code="CCC")

$location = Get-Location
$repo = "$($location)\communities-accelerator"

git clone --branch=$branch git@bitbucket.org:cloudgaia/communities-accelerator.git
#git clone git@bitbucket.org:cloudgaia/communities-accelerator.git
Set-Location -path $repo
python.exe "$($location)\deploy_diff_to_org.py"

#sfdx force:mdapi:deploy -d $code -u $org -w 10

Set-Location -Path $location

#Remove-Item -Path $repo -Recurse -Force