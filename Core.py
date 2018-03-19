# encoding: utf-8
#2018/01/22  Chao
import os
import stat
import os.path
import shutil
import time

##判断是否为junction

#kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
#FILE_ATTRIBUTE_REPARSE_POINT = 0x0400

#import ctypes
#from ctypes import wintypes

#def islink(path):
#    data = wintypes.WIN32_FIND_DATAW()
#    kernel32.FindClose(kernel32.FindFirstFileW(path, ctypes.byref(data)))
#    if not data.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT:
#        return False
#    return IsReparseTagNameSurrogate(data.dwReserved0)

#def IsReparseTagNameSurrogate(tag):
#    return bool(tag & 0x20000000)

#将某个文件夹下的所有文件复制到目标目录


def BackupFiles(sourceDir):#将文件夹加上bk后缀备份
    if os.path.exists(sourceDir):
        backupPath=sourceDir+'_bk'
        os.rename(sourceDir,sourceDir+'_bk')
        return backupPath
    else:
        backupPath=None
        return backupPath

def CheckConnection(netPath):
    if os.access(netPath,True):
        return True
    else:
        return False

def CopyFiles(sourceDir,targetDir):
    for file in os.listdir(sourceDir): 
         sourceFile = os.path.join(sourceDir, file) 
         targetFile = os.path.join(targetDir, file) 
         if os.path.isfile(sourceFile): 
             if not os.path.exists(targetDir): 
                 os.makedirs(targetDir)
                 print("Create path " + targetFile + " success\n",)                 
             if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))): 
                     print("Copying file " + targetFile + "...\n",)  
                     shutil.copyfile(sourceFile,targetFile)
                     #open(targetFile, "wb").write(open(sourceFile, "rb").read())
         if os.path.isdir(sourceFile): 
             First_Directory = False 
             CopyFiles(sourceFile, targetFile)
             print("Create path " + targetFile + " success\n",)

def CopyFolder(sourceDir,targetDir):
    folder=os.path.split(sourceDir)[1]
    tarPath=os.path.join(targetDir,folder)
    os.makedirs(tarPath)
    CopyFiles(sourceDir,tarPath)
    print("Copy "+folder+" to "+targetDir+" success")

def CreateSymlink(sourceDir,targetDir):#创建目录的符号链接
    #备份文件夹
    #os.rename("K:/GeneratedData/gameassets/cooked_durango-dev","K:/GeneratedData/gameassets/cooked_durango_bk")
    #os.rename(targetDir,targetDir+'.bk')
    if os.path.exists(targetDir):
        DeleteFlies(targetDir)

    #https://stackoverflow.com/questions/1143260/create-ntfs-junction-point-in-python
    #从CMD创建Juction
    dirToMake=targetDir.replace("/","\\")
    os.makedirs(dirToMake)
    #Windows命令行，cmd = "Mklink /J K:\GeneratedData\gameassets\cooked_durango-dev E:\GeneratedData\cooked_durango-dev"
    cmd = "Mklink /J %s %s"%(sourceDir,targetDir)
    os.system(cmd)
    print(cmd)
    print("Create junction link success")
    #from subprocess import run
    #run(cmd,shell=True)

    #kdll = ctypes.windll.LoadLibrary("kernel32.dll")
    #kdll.CreateSymbolicLinkA("D:\testdir", "D:\testdir_LINK",1)
    #kdll.CreateSymbolicLinkA("K:\GeneratedData\gameassets\cooked_durango-devtest", "E:\GeneratedData", 1)

    #kdll.CreateSymbolicLinkW(UR"K:\GeneratedData\gameassets\cooked_durango-devtest", UR"E:\GeneratedData\cooked_durango-dev", 1)
    #os.symlink(OriPath, TargetPath)
    #os.chdir('K:\GeneratedData\gameassets\')
    #os.rename('cooked_durango-dev','cooked_durango-dev.bk')
    #os.mkdir('cooked_durango-dev')

    #os.chdir('E:/GeneratedData')
    #os.mkdir('cooked_durango-dev')
    #os.symlink(r'K:/GeneratedData/gameassets/cooked_durango-dev','cooked_durango-dev')

def Delay(sec,action_str="Action"):
    #for t in xrange(5, 1, -1):
    for t in reversed(range(sec)):
        print("%s will start in %ss\r"%(action_str,t),)
        t-=1            
        time.sleep(1)
    print("                                                \r",)

#删除多层空文件夹
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

def FindFile(fileName,path,returntype="filename"):
    '''
    parameter "path":search file by string and return its full path
    parameter "bool":see if there are files include string in filename, if it is, return True
    parameter "filename"(default):return full file name include string 
    '''
    if returntype == "file":
        fileList=[]
        for file in os.listdir(path):
            if fileName in file:
                fileFullPath=os.path.join(path,file)
                fileList.append(fileFullPath)
        return fileList
    elif returntype == "bool":
        flag=False
        for file in os.listdir(path):
            if fileName in file:
                flag = True
        return flag
    elif returntype == "filename":
        for file in os.listdir(path):
            if fileName in file:
                return file

    elif returntype == "path":
        for file in os.listdir(path):
            if fileName in file:
                fileFullPath=os.path.join(path,file)
        return fileFullPath

    else:
        return None

def FixMyDurango():
    
    #cr.KiddingU()
    os.chdir(r"C:\Program Files (x86)\Microsoft Durango XDK\bin")

    os.system("xbdeploy.exe stop")
    os.system("taskkill /F /IM xbdeploy.exe")
    os.system("taskkill /F /IM xbrdevicesrv.exe")
    #os.system("pushd \"C:\\Program Files (x86)\\Microsoft Durango XDK\\bin\"")
    #os.system("xbdel xs:\\apps\\TR11_1.0.0.1_x64__ywaz7tst186jr\\root\\*.*")
    #os.system("xbdel xs:\\apps\\TR11_1.0.0.1_x64__ywaz7tst186jr\\root\\movies\\*.*")
    #os.system("xbrmdir xs:\\apps\\TR11_1.0.0.1_x64__ywaz7tst186jr\\root\\movies\\")
    #os.system("xbrmdir xs:\\apps\\TR11_1.0.0.1_x64__ywaz7tst186jr\\root\\")
    os.system("xbapp uninstall TR11OUTSOURCE_1.0.0.1_x64__ywaz7tst186jr")
    os.system("xbreboot")

def KiddingU(times=1000):
    for i in range(1,times):
        print ("Fuck*"+str(i))
        OpenFile(r"E:\Dev\test.txt")
        KillProcess("notepad.exe")
        print ("\n")

def KillProcess(process):
    try:
        cmd="taskkill /F /IM %s"%process
        os.system(cmd)

    except Exception:
        print(str(Exception))

def KillTRProcesses():
    msbuild="msbuild.exe"
    amtray="amtray.exe"
    assetmonitor="assetmonitor.exe"
    GameGUI="GameGUI.exe"
    GameGUID="GameGUID.exe"
    NetworkFileServer="NetworkFileServer.exe"
    supergraphx64="supergraphx64.exe"

    KillProcess(msbuild)
    KillProcess(amtray)
    KillProcess(assetmonitor)
    KillProcess(GameGUI)
    KillProcess(GameGUID)
    KillProcess(NetworkFileServer)
    KillProcess(supergraphx64)

def MoveFiles(sourceDir,targetDir):#将文件移动至目标文件夹
    #if sourceDir is not None:
        CopyFiles(sourceDir,targetDir)
        DeleteFlies(sourceDir)
        print("Transfer files success")
    #else:
        #print "Copy failed,please check copy path"
#删除列表中的所有文件

def MutiDelete(files):
    for file in files:
        try:
            os.remove(file)
            print("Delete file"+str(file))
        except Exception:
            os.chmod(file,stat.S_IWRITE)

def OpenFile(dir):
    try:
        os.startfile(dir)

    except Exception:
        print(str(Exception))

def StartGameGUI():
    cmd="D:\\tr11\\tr11_dev\\cdc\\bin\\cdcApplyEnv.exe -root=\"d:\\tr11\\tr11_dev\" -spawn=\"Gamegui.exe\""
    os.system(cmd)
