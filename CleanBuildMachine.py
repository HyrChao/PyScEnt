import os
import os.path
import stat


localRoot = "D:\ShareFolder\HourlyBigfile"

def DeleteEmptyFolder(dir):
    if os.path.isdir(dir):
        for folder in os.listdir(dir):
            DeleteEmptyFolder(os.path.join(dir, folder))
    if not os.listdir(dir):
        os.chmod(dir,stat.S_IWRITE)
        os.rmdir(dir)
    print('Delete empty folder: ' + dir)

def DeleteFlies(targetDir):
    for file in os.listdir(targetDir): 
        targetFile = os.path.join(targetDir,file)
        if os.path.isfile(targetFile): 
            try:
                os.remove(targetFile)
            except Exception:
                os.chmod(targetFile,stat.S_IWRITE)
                os.remove(targetFile)
            print("Deleting file "+  targetFile + " ...\r")
        if os.path.isdir(targetFile):
            if not os.listdir(targetFile):
                os.chmod(targetFile,targetFile)
                os.rmdir(targetFile)
            else:
                DeleteFlies(targetFile)
                print("Deleting path "+  targetFile + " ...\r")

#删除目录下的所有文件 
def Delete(target):
    if os.path.isfile(target):
        try:
            os.remove(target)
        except Exception:
            os.chmod(target,stat.S_IWRITE)
            os.remove(target)
    else:
        DeleteFlies(target)
        if os.path.exists(target):
            DeleteEmptyFolder(target)

def CleanLocal():
    bigfileMark="BF_TR11_"
    dirlist=os.listdir(localRoot)
    virsionArray=[]
    for dir in dirlist:
        filePath=os.path.join(localRoot,dir)
        if bigfileMark in dir:
            version=dir.split('_',4)[4]
            virsionArray.append(version)                   
        else:
            Delete(filePath)
            print("Delete extra local files success")
    virsionArray.sort()
    if len(virsionArray) > 6:
        virsionArray=virsionArray[:-6]  #slice 去除列表后三位
        for virsion in virsionArray:
            for dir in dirlist:
                if virsion in dir:
                    oldBigfilePath=os.path.join(localRoot,dir)
                    Delete(oldBigfilePath)
    else:
        pass

if  __name__ =="__main__":

    CleanLocal()