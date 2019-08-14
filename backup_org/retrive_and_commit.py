import os
import zipfile
import shutil
import datetime


def retrive_and_extract(deploydir,orgname,outputdir='tmpdir'):
    """retrive metadata from org and extract metadata form zip file"""
    shutil.rmtree(deploydir)
    os.mkdir(outputdir)
    cmd = 'sfdx force:mdapi:retrieve -r ' + outputdir + ' -u ' + orgname + ' -k package.xml'
    os.system(cmd)
    zfile = os.listdir(outputdir)[0]
    with zipfile.ZipFile(os.path.join(outputdir,zfile),'r') as datazip:
        datazip.extractall()
    os.rename(zfile.split('.zip')[0],deploydir)
    shutil.rmtree(outputdir)


if __name__ == '__main__':
    retrive_and_extract('src','edge5')
    os.system('git add .')
    os.system('git commit -m ' + datetime.datetime.today().isoformat())
    os.system('git push origin master')