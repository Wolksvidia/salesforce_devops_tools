Param([string] $org="sbx_cg", [string] $branch="master")
#Set location of the git project
Set-Location -path "C:\Users\Emiliano Fama\Documents\Repositorios\bitbucket\cg_internal_org"
git checkout $branch

#Delete folder
$location = Get-Location
$folder = "$($location)\unpackaged"
Remove-Item -Path $folder -Recurse -Force

#Retrieve metadata
sfdx force:mdapi:retrieve -r $location -u $org -k package.xml

#Extract metadata 
Set-Location -path $location 
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
git push origin master