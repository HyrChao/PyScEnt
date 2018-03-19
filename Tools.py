# encoding: utf-8
#2018/01/22  Chao
import os
import os.path
import Core as cr
import DeployTool as dt

    #os.chdir("E:\Dev")
    #os.startfile("test.txt")

    #os.chdir(r"C:\Program Files (x86)\Microsoft Durango XDK\bin")
    #subprocess.call("xbdeploy.exe stop")
    #subprocess.call(cmd2)
    #subprocess.call(cmd3)
    #subprocess.call(cmd4)
    #subprocess.call(cmd5)
    #subprocess.call(cmd6)
    #subprocess.call(cmd7)
    #subprocess.call(cmd8)
    #subprocess.call(cmd9)
    #subprocess.call(cmd10)


def GetBigfileMannager(tar=None,src=None):
    if tar and src is not None:
        if os.path.isdir(tar) and os.path.isdir(src):
            bf=dt.Bigfile(tar,src)
            return bf
        else:
            print("path is wrrong,please check")
            return None
    else:
        bf=dt.Bigfile()
        return bf

def AutoFix():
    cr.KillTRProcesses()
    cr.FixMyDurango()
    print ("Fix complete")
    return True

def AutoDeploy():
    bf=dt.Bigfile()
    bf.AutoDeploy()

def AutoCopyBigfile():
    bf=dt.Bigfile()
    bf.CopyLatesstToLocal()

def DeleteGenerateData(mode,fileName=None,path=r"D:\tr11\tr11_dev\GeneratedData\gameassets\cooked_durango-dev"):
    if mode == "Wwise":
        try:
            cr.DeleteFlies(r"D:\tr11\tr11_dev\GeneratedData\gameassets\cooked_durango-dev\wwise")
        except Exception:
            print("Wwise")
    elif mode == "Simplygon":
        try:
            cr.DeleteFlies(r"D:\tr11\tr11_dev\GeneratedData\gameassets\build_DURANGO-DEV\mesh")
        except Exception:
            print("Simplygon")
    elif mode == "Filename":
        filesToDelete=[]
        filesToDelete=cr.FindFile(fileName,path,"file")
        print("Here is flie list to delete:"+str(filesToDelete))
        cr.MutiDelete(filesToDelete)
    else:
        print("Wrong parameter")
            
def SetupLink(sourcePath,targetPath):
    src=sourcePath.replace("/","\\")
    tar=targetPath.replace("/","\\")
    #print(a)
    print(src)
    print(tar)
    backupPath=cr.BackupFiles(src)
    cr.CreateSymlink(src,tar)
    cr.MoveFiles(backupPath,src)
    print("Complete!")
    return True

def Test():
    print("test")


if  __name__ =="__main__":

    AutoFix()
