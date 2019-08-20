import os
import shutil
import string
import platform


""" >> -meta.xml necesario para classes triggers pages
>> .cmp para aura
>> .js para lwc """


def make_dirtree(fpath, basedir):
    #spliter es / en linux o \\ en windows
    if platform.system() == 'Windows':
        spliter = '\\'
    else:
        spliter = '/'
    dtree = basedir
    bdir = os.path.dirname(fpath)
    sptdir = bdir.split(spliter)
    sptdir[0] = basedir
    if not os.path.exists(spliter.join(sptdir)):
        sptdir = sptdir[1:]
        for ndir in sptdir:
            if not os.path.exists(dtree):
                os.mkdir(dtree)
            dtree = spliter.join([dtree,ndir])
        os.mkdir(dtree)


def build_diff_files(inputdir,outputdir,differ='origin/master',inputfile='diff.txt'):
    #seteo del spliter dependiendo del SO
    cmd = 'git diff --name-status ' + differ + ' >> ' + inputfile
    out = os.system(cmd)
    ldiff = []
    lfront = []
    ldel = []
    try:
        with open(inputfile, "r") as rfile:
            for line in rfile:
                #parche para eliminar caracteres no visibles, quitar len(line)-1 en linux
                if platform.system() == 'Windows':
                    fpath = os.path.normpath(line[2:len(line)-1])
                else:
                    fpath = os.path.normpath(line[2:len(line)])
                if inputdir in fpath:
                    if '-meta.xml' not in fpath:
                        if line[:1] != 'D':
                            if ('.cls' in fpath) | ('.trigger' in fpath) | ('.page' in fpath) | ('.resource' in fpath): 
                                ldiff.append(fpath)
                                ldiff.append(fpath+'-meta.xml')
                            elif ('aura' in fpath) | ('lwc' in fpath):
                                ndir = os.path.dirname(fpath)
                                if ndir not in lfront:
                                    lfront.append(os.walk(ndir))    
                            else:
                                ldiff.append(fpath)
                            
                        else:
                            ldel.append(fpath)
    except IOError:
        pass

    for ffront in lfront:
        for path, i, listfile in ffront:
            for afile in listfile:
                ldiff.append(os.path.join(path,afile))
    
    for afile in ldiff:
        make_dirtree(afile,outputdir)
        ofile = afile.replace(inputdir,outputdir)
        # sptdir = afile.split(spliter)
        # sptdir[0] = outputdir
        #shutil.copy(afile,spliter.join(sptdir))
        shutil.copy(os.path.normpath(afile),os.path.normpath(ofile))


if __name__ == '__main__':
    build_diff_files('src','CCC')