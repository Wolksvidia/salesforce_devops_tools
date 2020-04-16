Backup Org Interna Bitbucket Pipelines
======================================
## DescripciÃ³n
El objetivo es realizar un backup de la metadata de la org productiva. El pipeline utiliza una Connected app o authurl que autoriza CLI de Salesforce para realizar un retrieve de la metadata, descomprime el archivo zip obtenido, luego realiza un commit de los cambios y por ultimo un push al repositorio.
## Requerimientos para utilizar metodo AuthURL
* #### Obtener AuthURL
> * Autenticar la org localmente con el comando, si es sandbox, sfdx force:auth:web:login -a ALIAS -r https://test.salesforce.com
> * Guardar la AuthUrl que se obtiene con el comando sfdx force:org:display -u ALIAS --verbose, tiene la estructura **force://clientId:clientSecret:refreshToken@instanceUrl**

* #### Agregar la authurl a las variables de entorno
> * AUTHURL
## EjecuciÃ³n
  Ejecutar el pipeline **backup** desde el **branch de Master**

## Requerimientos para utilizar metodo JWT
* #### Generacion de un cetificado sef-signed
Se deben generar dos archivos "server.key" y "server.crt", desde Git Bash con los siguientes comandos:
> * openssl genrsa -des3 -passout pass:mypassword -out server.pass.key 2048
> * openssl rsa -passin pass:mypassword -in server.pass.key -out server.key
> * Borrar "server.pass.key"
> * openssl req -new -key server.key -out server.csr
> * openssl x509 -req -sha256 -days 365 -in server.csr -signkey server.key -out server.crt
* #### Crear una Connected App en la ORG
Referencia para la creacion _https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_auth_connected_app.htm_
* #### Agregar la consumer key y el user admin a las variables de entorno
> * CONSUMER_KEY_PROD
> * USER_NAME_PROD
## EjecuciÃ³n
  Ejecutar el pipeline **backup_old** desde el **branch de Master** 

Backup Org Interna Script PowerShell
====================================
## DescripciÃ³n
El objetivo es realizar un backup de la metadata de la org productiva. El script utiliza la CLI de Salesforce para realizar un retrieve de la metadata, descomprime el archivo zip obtenido, luego realiza un commit de los cambios y por ultimo un push al repositorio.
## Requerimientos
* #### Instalar Salesforce CLI
Instalar la Command Line Tool desde _https://developer.salesforce.com/tools/sfdxcli_
* #### Instalar GIT
Instalar la ultima versiÃ³n de git desde _https://git-scm.com/_
* #### Clonar el repositorio
Clonar el repositorio **git clone git@bitbucket.org:cloudgaia/cg_internal_org.git**
* #### Log-in Org y seteo de alias
Realizar el login de la org y asignar un alias con el siguiente comando:
  **sfdx force:auth:web:login -a "ALIAS"**
* #### Editar script
  * Setear el path del repositorio en: **Param([string] $repo="<Path>"**
  * Asignar al parametro $org el alias configurado anteriormente en: **Param([string] $org="sbx_cg"...**
## EjecuciÃ³n
  Ejecutar el script backup_org.ps1 desde una consola de PowerShell