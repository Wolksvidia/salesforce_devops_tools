Param([string] $org="sbx_cg", [string] $branch="master", [string] $repo="C:\Users\Emiliano Fama\Documents\Repositorios\bitbucket\cg_internal_org",
[string] $manifest="package.xml")

#Set location of the git project
Set-Location -path $repo
git checkout $branch

#Delete folder
$location = Get-Location
$folder = "$($location)\unpackaged"
If ((Test-Path $folder) -eq $True) {
    Remove-Item -Path $folder -Recurse -Force
}

#Retrieve metadata
sfdx force:mdapi:retrieve -r $location -u $org -k $manifest

#Extract metadata 
$Unzip = New-Object -ComObject Shell.Application
$FileName = "unpackaged.zip"
$ZipFile = $Unzip.NameSpace((Get-Location).Path + "\$FileName") 
$Destination = $Unzip.namespace((Get-Location).Path) 
$Destination.Copyhere($ZipFile.items())

#Remove zip file
Remove-Item -Path $FileName

#Commit new metadata
$date = Get-Date -Format "dd-MM-yyyy"
git add .
git commit -m $date
git push origin $branch