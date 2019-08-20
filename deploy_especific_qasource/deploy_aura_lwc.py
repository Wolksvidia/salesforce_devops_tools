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


def remove_cms_references(nddir,namespace,new_namespace=None):
    """Remove CMS references from Aura and Classes"""
    aurapath = os.path.join(nddir,'aura')
    if os.path.exists(aurapath):
        auradirs = os.listdir(aurapath)
        for aura in auradirs:
            cmppath = os.path.join(aurapath,aura)
            files = os.listdir(cmppath)
            for afile in files:
                if '.cmp' in afile:
                    with open(os.path.join(cmppath,afile), 'r') as f:
                        dataf = f.read()
                    if namespace+':' in dataf:
                        print(afile)
                        if new_namespace is None:
                            datan = dataf.replace(namespace+':','c:')
                        else:
                            datan = dataf.replace(namespace+':',new_namespace+':')
                        os.remove(os.path.join(cmppath,afile))
                        with open(os.path.join(cmppath,afile), 'w') as f:
                            f.write(datan)
    classpath = os.path.join(nddir,'classes')
    if os.path.exists(classpath):
        classes = os.listdir(classpath)
        for aclass in classes:
            if '-meta.xml' not in aclass:
                with open(os.path.join(classpath,aclass),'r') as f:
                    dataf = f.read()
                if namespace+'__' or namespace+'.' in dataf:
                    print(aclass)
                    if new_namespace is None:
                        datan = dataf.replace(namespace+'__','')
                        datam = datan.replace(namespace+'.','')
                    else:
                        datan = dataf.replace(namespace+'__',new_namespace+'__')
                        datam = datan.replace(namespace+'.',new_namespace+'.')
                    os.remove(os.path.join(classpath,aclass))
                    with open(os.path.join(classpath,aclass), 'w') as f:
                        f.write(datam)
            # else:
            #     with open(os.path.join(classpath,aclass),'r') as f:
            #         dataf = f.read()
            #     with open(os.path.join(classpath,aclass), 'w') as f:
            #         for line in dataf:
            #             if 'packageVersions>' or '<minorNumber>' or '<majorNumber>' not in line:
            #                 f.write(line)



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
    remove_cms_references('src','DiageoCMS')
    #remove_cms_references('src','DiageoCMS','CMSTESTQA')
    deploy_mdapi('src','QAsource')
    #deploy_mdapi('src','TestCMSpackage')