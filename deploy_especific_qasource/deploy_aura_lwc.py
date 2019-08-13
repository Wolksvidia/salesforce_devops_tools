import os
import zipfile
import shutil


def retrive_and_extract(deploydir,orgname,outputdir='tmpdir'):
    """retrive metadata from org and extract metadata form zip file"""
    os.mkdir(outputdir)
    cmd = 'sfdx force:mdapi:retrieve -r ' + outputdir + ' -u ' + orgname + ' -k package.xml'
    os.system(cmd)
    zfile = os.listdir(outputdir)[0]
    with zipfile.ZipFile(os.path.join(outputdir,zfile),'r') as datazip:
        datazip.extractall()
    os.rename(zfile.split('.zip')[0],deploydir)
    shutil.rmtree(outputdir)


def remove_cms_references(nddir):
    """Remove CMS references from Aura and Classes"""
    aurapath = os.path.join(nddir,'aura')
    auradirs = os.listdir(aurapath)
    for aura in auradirs:
        cmppath = os.path.join(aurapath,aura)
        files = os.listdir(cmppath)
        for afile in files:
            if '.cmp' in afile:
                with open(os.path.join(cmppath,afile), 'r') as f:
                    dataf = f.read()
                if 'DiageoCMS:' in dataf:
                    print(afile)
                    datan = dataf.replace('DiageoCMS:','c:')
                    os.remove(os.path.join(cmppath,afile))
                    with open(os.path.join(cmppath,afile), 'w') as f:
                        f.write(datan)
    classpath = os.path.join(nddir,'classes')
    classes = os.listdir(classpath)
    for aclass in classes:
        if '-meta.xml' not in aclass:
            with open(os.path.join(classpath,aclass),'r') as f:
                dataf = f.read()
            if 'DiageoCMS__' or 'DiageoCMS.' in dataf:
                print(aclass)
                datan = dataf.replace('DiageoCMS__','')
                datam = datan.replace('DiageoCMS.','')
                os.remove(os.path.join(classpath,aclass))
                with open(os.path.join(classpath,aclass), 'w') as f:
                    f.write(datam)



def remove_non_related_dba(mddir):
    """"Read source directory and remove all components non-related to DBA project
    and replace DiageoCMS dependecy"""
    aurapath = os.path.join(mddir,'aura')
    #lwcpath = os.path.join(mddir,'lwc')
    auradirs = os.listdir(aurapath)
    rmaura = []
    for aura in auradirs:
        if 'DBA_' not in aura:
            rmaura.append(os.path.join(aurapath,aura))
        else:
            cmppath = os.path.join(aurapath,aura)
            files = os.listdir(cmppath)
            for afile in files:
                if '.cmp' in afile:
                    with open(os.path.join(cmppath,afile), 'r') as f:
                        dataf = f.read()
                    # if 'aura:component' and 'controller=' in dataf:
                    #     rmaura.append(os.path.join(aurapath,aura))
                    if 'DiageoCMS:' in dataf:
                        print(afile)
                        datan = dataf.replace('DiageoCMS:','c:')
                        os.remove(os.path.join(cmppath,afile))
                        with open(os.path.join(cmppath,afile), 'w') as f:
                            f.write(datan)
    #remove components           
    for adir in rmaura:
        shutil.rmtree(adir)


def deploy_mdapi(source,orgname):
    """Deploy metadata, then remove source directory"""
    cmd = 'sfdx force:mdapi:deploy -d ' + source + ' -u ' + orgname + ' -w 10'
    os.system(cmd)
    shutil.rmtree(source)


if __name__ == '__main__':
    retrive_and_extract('src','edge5')
    remove_cms_references('src')
    deploy_mdapi('src','QAsource')