# encoding: utf-8
#2018/01/15  Chao
import os
import stat
import os.path
import shutil

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

#删除目录下的所有文件 
def DeleteFlies(target):
    if os.path.isfile(target):
        try:
            os.remove(target)
        except Exception:
            os.chmod(target,stat.S_IWRITE)
            os.remove(target)
    else:
        DeleteFliesInFolder(target)
        if os.path.exists(target):
            DeleteEmptyFolder(target)

def DeleteFliesInFolder(targetDir):
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
                DeleteFliesInFolder(targetFile)
                print("Deleting path "+  targetFile + " ...\r")

#删除多层空文件夹
def DeleteEmptyFolder(dir):
    if os.path.isdir(dir):
        for folder in os.listdir(dir):
            DeleteEmptyFolder(os.path.join(dir, folder))
    if not os.listdir(dir):
        os.chmod(dir,stat.S_IWRITE)
        os.rmdir(dir)
    print('Delete empty folder: ' + dir)

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

def BackupFiles(sourceDir):#备份要被link的文件夹
    if os.path.exists(sourceDir):
        backupPath=sourceDir+'_bk'
        os.rename(sourceDir,sourceDir+'_bk')
        return backupPath
    else:
        backupPath=None
        return backupPath

def CopyFilesIn(sourceDir,targetDir):#将备份文件拷贝至目标文件夹
    #if sourceDir is not None:
        CopyFiles(sourceDir,targetDir)
        DeleteFlies(sourceDir)
        print("Transfer files success")
    #else:
        #print "Copy failed,please check copy path"

def Main():
    print("===========================================================\n")
    print("|   ATTENTION:You must run this script as admin!          |\n")
    print("===========================================================\n")
    print("Start(1)  Quit(0) \n")
    print("Please input:") 
    flag = True

    LinkPath=r'D:\tr11\tr11_dev\assets'
    TargetPath=r'E:\tr11\tr11_dev\assets'
    #Win格式路径替换为Unix格式
    while (flag): 
         answer = input()
         if  answer == '0': 
             flag = False 
         elif answer == '1': 
             #if islink(LinkPath):
             #    os.remove(sourceDir)
             #    print "Junction link already exists"
            BackupPath=BackupFiles(LinkPath)
            CreateSymlink(LinkPath,TargetPath)
            CopyFilesIn(BackupPath,TargetPath)
            print("Complete!") 
         else: 
             print("Please input correct command") 

def SetupLink(sourcePath,targetPath):
    src=sourcePath.replace("/","\\")
    tar=targetPath.replace("/","\\")
    #print(a)
    print(src)
    print(tar)
    backupPath=BackupFiles(src)
    CreateSymlink(src,targetPath)
    CopyFilesIn(backupPath,src)
    print("Complete!") 

def Auto():
    LinkPath=r'D:\tr11\tr11_dev\assets'
    TargetPath=r'E:\tr11\tr11_dev\assets'
    BackupPath=BackupFiles(LinkPath)
    CreateSymlink(LinkPath,TargetPath)
    CopyFilesIn(BackupPath,TargetPath)
    print("Complete!") 

def Test():
    delPath=r"D:\tr11\tr11_dev\deltest1"
    DeleteFlies(delPath)

if  __name__ =="__main__":#主函数
    Main()
