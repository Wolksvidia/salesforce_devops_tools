# Parameter help description
Param([string] $org="efadev", [string] $branch="development", [string] $code="src")

$location = Get-Location
$repo = "$($location)\communities-accelerator"

#git clone --branch=$branch --single-branch git@bitbucket.org:cloudgaia/communities-accelerator.git
git clone git@bitbucket.org:cloudgaia/communities-accelerator.git
Set-Location -path $repo
git checkout $branch

python.exe "$($location)\diff_maker\diff_maker.py"

sfdx force:mdapi:deploy -d $code -u $org -w 10

Set-Location -Path $location

Remove-Item -Path $repo -Recurse -Force