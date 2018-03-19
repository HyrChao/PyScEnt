# encoding: utf-8
#2017/11/23 Chao  

import os
import os.path

global wwiseGenerateddataPath
global cookedGeneratedDataPath

wwiseGenerateddataPath="K:\GeneratedData\gameassets\cooked_durango-dev\wwise"
cookedGeneratedDataPath="K:\GeneratedData\gameassets\cooked_durango-dev"

def FindFileByName(filename,path=cookedGeneratedDataPath,):
    for file in os.listdir(cookedGeneratedDataPath): 
         targetFile = os.path.join(cookedGeneratedDataPath,  file)
         fileArray=[]
         if os.path.isfile(targetFile): 
             if filename in targetFile: 
                 fileArray.append(targetFile)
         if os.path.isdir(targetFile): 
             FindFileByName(filename, targetFile)
    return fileArray

def CopyFiles(bigfile,localfolder):
    for file in os.listdir(bigfile): 
         sourceFile = os.path.join(bigfile,  file) 
         targetFile = os.path.join(localfolder,  file) 
         if os.path.isfile(sourceFile): 
             if not os.path.exists(localfolder): 
                 os.makedirs(localfolder)
                 print("Create path " + targetFile + " success\n",)                 
             if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))): 
                     print("Copying file " + targetFile + "...\n",)  
                     shutil.copyfile(sourceFile,targetFile)
                     #open(targetFile, "wb").write(open(sourceFile, "rb").read())
         if os.path.isdir(sourceFile): 
             First_Directory = False 
             CopyFiles(sourceFile, targetFile)
             print("Create path " + targetFile + " success\n",)

 
def DeleteFlies(targetDir):
    for file in os.listdir(targetDir): 
        targetFile = os.path.join(targetDir,file)
        if os.path.isfile(targetFile): 
            os.remove(targetFile)
            print("Deleting file "+  targetFile + " ...\r")
        if os.path.isdir(targetFile):
            if not os.listdir(targetFile):
                os.rmdir(targetFile)
            else:
                DeleteFlies(targetFile)
                print("Deleting path "+  targetFile + " ...\r")

#删除目录下的所有文件
def DeleteAllFlies(target):
    if os.path.isfile(target):
        os.remove(target)
    else:
        DeleteFlies(target)
        if os.path.exists(target):
            DeleteEmptyFolder(target)

def FixWwise():
    DeleteAllFlies(wwiseGenerateddataPath)

def FixGeneratedDataByName():
    filename=input("Please input file name:")
    errfiles=FindFileByName(filename)
    print(errfiles)