import os
import os.path as pth
import sys, shutil

# Level search alg
# Does not follow symlinks
def clearPythonCaches(directory,recursiveley=True,depth=-1):
    path = pth.abspath(directory)
    files=[]
    for new_dirs in os.listdir(path):
        new_dir = pth.abspath(pth.join(path,new_dirs))
        if pth.isdir(new_dir) and not pth.islink(new_dir) and (new_dirs not in  ['__pycache__','..','.','.git','.vscode','.pytest_cache']):
            files+=[new_dirs]
    i=0
    print(files)
    while True:
        
        for cache in (pth.abspath(pth.join(path,'__pycache__')),pth.abspath(pth.join(path,'.pytest_cache'))):
            if pth.exists(cache) and pth.isdir(cache):
                if  pth.islink(cache):
                    os.remove(cache)
                else:
                    shutil.rmtree(cache)
        
        if files[i:] == []:
            break
        
        path = files[i]
        ext = []
        for new_dirs in os.listdir(path):
            new_dir = pth.abspath(pth.join(path,new_dirs))
            if pth.isdir(new_dir) and not pth.islink(new_dir) and (new_dirs not in  ['__pycache__','..','.','.git','.vscode','.pytest_cache']):
                ext+=[new_dir]
        files+=ext   
        
        
        i+=1
        # print(files)
