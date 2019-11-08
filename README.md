Backup Org Interna CloudGaia
============================

## Descripción
El objetivo es realizar un backup periódico de la metadata de la org productiva. El script utiliza la CLI de Salesforce para realizar un retrieve de la metadata, descomprime el archivo zip obtenido, luego realiza un commit de los cambios y por ultimo un push al repositorio.

## Requerimientos
* #### Instalar Salesforce CLI
Instalar la Command Line Tool desde _https://developer.salesforce.com/tools/sfdxcli_
* #### Instalar GIT
Instalar la ultima versión de git desde _https://git-scm.com/_
* #### Clonar el repositorio
Clonar el repositorio **git clone git@bitbucket.org:cloudgaia/cg_internal_org.git**
* #### Log-in Org y seteo de alias
Realizar el login de la org y asignar un alias con el siguiente comando:
  sfdx force:auth:web:login -a "ALIAS"
* #### Editar script
  * Setear el path del repositorio en: **Set-Location -path "<Path>"**
  * Asignar al parametro $org el alias configurado anteriormente en: **Param([string] $org="sbx_cg"...**

## Ejecución
  Ejecutar el script backup_org.ps1 desde una consola de PowerShell