# encoding: utf-8
#2017/11/09  Chao

 #**
 #
 # ━━━━━━神兽出没━━━━━━
 # 　　　┏┓　　　┏┓
 # 　　┏┛┻━━━┛┻┓
 # 　　┃　　　　　　　┃
 # 　　┃　　　━　　　┃
 # 　　┃　┳┛　┗┳　┃
 # 　　┃　　　　　　　┃
 # 　　┃　　　┻　　　┃
 # 　　┃　　　　　　　┃
 # 　　┗━┓　　　┏━┛Code is far away from bug with the animal protecting
 # 　　　　┃　　　┃    神兽保佑,代码无bug
 # 　　　　┃　　　┃
 # 　　　　┃　　　┗━━━┓
 # 　　　　┃　　　　　　　┣┓
 # 　　　　┃　　　　　　　┏┛
 # 　　　　┗┓┓┏━┳┓┏┛
 # 　　　　　┃┫┫　┃┫┫
 # 　　　　　┗┻┛　┗┻┛
 # 
 #
 # ━━━━━━感觉萌萌哒━━━━━━
 
import os
import os.path
import shutil
import sys
import time



#class Bigfile(object):

#    localRootFolder
#    netRootFolder
#    xdkpath
#    gametitle
#    appid
#    latestVersion
#    latestLocalVersion
#    latestBigfileNetPath
#    latestBigfileLocalPath

#    def __init__(self):



def Auto():
    global localRootFolder
    global netRootFolder
    global xdkpath
    global gametitle
    global appid
    global latestVersion
    global latestLocalVersion
    global latestBigfileNetPath
    global latestBigfileLocalPath

    localRootFolder="E:\BigFiles"
    netRootFolder=r"\\CNSHAW1694\ShareFolder\HourlyBigfile"
    #netRootFolder = netRootFolderWin.replace("\\", "\\\\") #windows网络位置格式转换为unix格式
    xdkpath=r"C:\Program Files (x86)\Microsoft Durango XDK\bin"
    gametitle="TR11OUTSOURCE_1.0.0.1_x64__ywaz7tst186jr"
    appid="TR11OUTSOURCE_ywaz7tst186jr!TR11.App"

    onlineMode=CheckConnection(netRootFolder)
    CheckLocalPath(localRootFolder)
    latestLocalVersion=GetLatestLocalVersion()
    latestBigfileLocalPath=GetLatetLocalBigfilePath()

    if onlineMode:
        print("Connect to build machine success, copying latest version...")
        CopyAndDeployLatest()
        DeleteBackupBigfiles()
    else:
        print("Connect to build machine faild, reconnecting...")
        Reconnect(netRootFolder)
        CopyAndDeployLatest()
        DeleteBackupBigfiles()

def Main():
    global localRootFolder
    global netRootFolder
    global xdkpath
    global gametitle
    global appid
    global latestVersion
    global latestLocalVersion
    global latestBigfileNetPath
    global latestBigfileLocalPath


    localRootFolder="E:\BigFiles"
    netRootFolder=r"\\CNSHAW1694\ShareFolder\HourlyBigfile"
    #netRootFolder = netRootFolderWin.replace("\\", "\\\\") #windows网络位置格式转换为unix格式
    xdkpath=r"C:\Program Files (x86)\Microsoft Durango XDK\bin"
    gametitle="TR11OUTSOURCE_1.0.0.1_x64__ywaz7tst186jr"
    appid="TR11OUTSOURCE_ywaz7tst186jr!TR11.App"

    onlineMode=CheckConnection(netRootFolder)
    CheckLocalPath(localRootFolder)
    latestLocalVersion=GetLatestLocalVersion()
    latestBigfileLocalPath=GetLatetLocalBigfilePath()

    if len(sys.argv) >=2:
        print("Current mode:"+sys.argv[1])

        if sys.argv[1]=="-auto":
            
            if onlineMode:
                print("Connect to build machine success, copying latest version...")
                CopyAndDeployLatest()
                DeleteBackupBigfiles()
            else:
                print("Connect to build machine faild, reconnecting...")
                Reconnect(netRootFolder)
                CopyAndDeployLatest()
                DeleteBackupBigfiles()

        else:
            Select_NoGUI(onlineMode)

    else:
        Select_NoGUI(onlineMode)

#主函数
if  __name__ =="__main__":

    Main()

#win和unix之间的格式转换
def Info():
    print("\n")
    print("======================================================================================================\n")
    print("Copy latest version to local and deploy                 (1)   |  Deploy from local latest bigfile(2)\n")
    print("Dirctly deploy latest from build machine(cause net jam) (3)   |             Check bigfile version(4)\n")
    print("Clean local bigfile data(reserve 2 newest bigfiles)     (5)   |          Check&refresh connection(6)\n")
    print("                                                                                                      \n")
    print("                                                                                             Quit(0)\n")
    print("======================================================================================================\n")          
    print("\n")

def UniformPath(path,platform):
    #windows本地位置格式转换为unix格式
    if platform=="win":
        return path.replace("\\","/")
    #unix本地位置格式转化为windows格式
    if platform=="unix":
        return path.replace("/","\\")
    else:
        return False

def Delay(sec,action_str="Action"):
    #for t in xrange(5, 1, -1):
    for t in reversed(range(sec)):
        print("%s will start in %ss\r"%(action_str,t),)
        t-=1            
        time.sleep(1)
    print("                                                \r",)
                
#查找一级目录
def CheckConnection(netPath):
    if os.access(netPath,True):
        print("------------------------------------------------------------------------------------------------------")
        print("Access to "+netPath+" success")
        print("------------------------------------------------------------------------------------------------------")
        global latestVersion #函数内部需再次声明一次global
        global latestBigfileNetPath
        latestVersion=GetLatestVersion()
        latestBigfileNetPath=GetLatestBigfilePath()
        return True
    else:
        print("---------------------------------FAILED---------------------------------------------------------------")
        print("FAILED to access "+netPath+" please check your connection")
        print("------------------------------------------------------------------------------------------------------")
        return False

def Reconnect(netPath):
    if os.access(netPath,True):
        global latestVersion #函数内部需再次声明一次global
        global latestBigfileNetPath
        latestVersion=GetLatestVersion()
        latestBigfileNetPath=GetLatestBigfilePath()
        print("------------------------------------------------------------------------------------------------------")
        print("Access to "+netPath+" success")
        print("------------------------------------------------------------------------------------------------------")
    else:
        print("------------------------------------------------------------------------------------------------------")
        print("Failed to access "+netPath+" please check your connection")
        print("------------------------------------------------------------------------------------------------------")
        Delay(600,"Reconnect")
        Reconnect(netPath)



def FindFile(path,str,returntype="filename"):
    '''
    parameter "path":search file by string and return its full path
    parameter "bool":see if there are files include string in filename, if it is, return True
    parameter "filename"(default):return full file name include string 
    '''
    if returntype == "path":
        for file in os.listdir(path):
            if str in file:
                return os.path.join(path,file)
    elif returntype == "bool":
        flag=False
        for file in os.listdir(path):
            if str in file:
                flag = True
        return flag
    elif returntype == "filename":
        for file in os.listdir(path):
            if str in file:
                return file

#检测本地bigfile文件夹是否存在，文件夹中是否有废文件
def CheckLocalPath(localpath):
    localPathUnix=UniformPath(localpath,"win")
    bigfileMark="filetiger"
    if not os.path.exists(localPathUnix):
        os.makedirs(localPathUnix)
    dirlist=os.listdir(localpath)
    for file in dirlist:
        filepath=os.path.join(localpath,file)
        if bigfileMark in file:
            if not CheckBigfileComplement(filepath):
                DeleteAllFlies(filepath)
                print("Delete imcomplete local files success")
        else:
            DeleteAllFlies(filepath)
            print("Delete extra local files success")

def DeleteBackupBigfiles():
    bigfileCount=0
    for i in os.listdir(localRootFolder):
        if "filetiger" in i:
            bigfileCount+=1
    if bigfileCount >=3:
        oldVersion=GetLatestLocalVersion(True)
        oldBigfilePath=FindFile(localRootFolder,oldVersion,"path")
        DeleteAllFlies(oldBigfilePath)
        DeleteBackupBigfiles()
    else:
        print("Backup files less than two")

#卸载xbox游戏
def UninstallXboxGame(Gametitle):
    #@echo Uninstall tr11 bigfiles... 
    #xbapp uninstall TR11OUTSOURCE_1.0.0.1_x64__ywaz7tst186jr
    print("Uninstalling old game version")
    cmd="xbapp uninstall %s"%Gametitle
    #os.system("cd "+xdkpath)
    os.chdir(xdkpath)
    uninstallResault=os.popen(cmd)
    print(uninstallResault)

#从bigfile安装xbox游戏
def DeployXboxGame(Gametitle,sourceFolder):
    #@echo Deploying tr11, please wait...
    #xbapp deploy E:\filetiger_TR11_18h09_durango_C194642_A194642
    print("Installing new game version,please wait...(depend on network states, might take more than 15 mins)")
    sourceFolderWin=UniformPath(sourceFolder,"unix")
    os.chdir(xdkpath)
    #os.system("cd "+xdkpath)
    cmd="xbapp deploy %s"%sourceFolder
    print(cmd)
    deployResault=os.popen(cmd)
    print(deployResault)
    if deployResault=="The operation completed successfully.":
        print("The operation completed successfully.")
        return True

#启动xbox游戏
def LaunchGame(appid):
    #@echo launching game
    #xbapp launch TR11OUTSOURCE_1.0.0.1_x64__ywaz7tst186jr
    print("launching game...")
    os.chdir(xdkpath)
    #os.system("cd "+xdkpath)
    cmd="xbapp launch %s"%appid
    #TR11OUTSOURCE_ywaz7tst186jr!TR11.App
    os.system(cmd)

#检测bigfile是否完整build
def CheckBuildComplement(buildFilePath):
    completeMarkFile="Changelists.txt"
    for file in os.listdir(buildFilePath):
        if completeMarkFile in file:
            return True
        else:
            return False

def CheckBigfileComplement(bigfilePath):
    completeMarkFile="TR11.exe"
    complete=False
    for file in os.listdir(bigfilePath):
        if completeMarkFile in file:
            complete=True
    return complete

#获取网络上最新Build完整版本的bigfile
def GetLatestVersion(reverse=False):
    '''
    default:reverse=False
    True:Get oldest local version
    False:Get latest local version
    '''
    netDirList=os.listdir(netRootFolder)
    numArray=[]
    for file in netDirList:
        #BF_TR11_13h58_durango_C196744_A196744
        buildNum=file.split('_',4)[4]#以‘_’为标识分割4次并取第5个元素
        numArray.append(buildNum)
    if len(numArray)==0:
        print("There are currently no bigfiles in build machine")
        return None
    numArray.sort()
    oldertNum=numArray[0]
    numArray.sort(reverse=True)#倒序排序
    latestNum=numArray[0]
    #检测服务器上文件是否完整build
    if reverse==False:
        for file in netDirList:
            if latestNum in file:
                if CheckBuildComplement(os.path.join(netRootFolder,file)) is True:
                    return latestNum
                else:
                    latestNum=numArray[1]
                    return latestNum
    else:
        return oldertNum

def GetLatestLocalVersion(reverse=False):
    '''
    default:reverse=False
    True:Get oldest local version
    False:Get latest local version
    '''
    folderLocation=localRootFolder
    numArray=[]
    for file in os.listdir(folderLocation):
        #filetiger_TR11_11h57_durango_C196245_A196245
        buildNum=file.split('_',4)[4]#以‘_’为标识分割4次并取第5个元素
        numArray.append(buildNum)
    if len(numArray)==0:
        print("There are currently no bigfiles in local bigfile folder")
        return None
    numArray.sort()
    oldertNum=numArray[0]
    numArray.sort(reverse=True)#倒序排序
    latestNum=numArray[0]
    if reverse==False:
        bigfileLocation=FindFile(folderLocation,"_durango_"+latestNum,"path")
        if CheckBigfileComplement(bigfileLocation):
            return latestNum
        else:
            DeleteAllFlies(bigfileLocation)
            GetLatestLocalVersion()
    else:
        bigfileLocation=FindFile(folderLocation,"_durango_"+oldertNum,"path")
        if CheckBigfileComplement(bigfileLocation):
            return oldertNum
        else:
            DeleteAllFlies(bigfileLocation)
            GetLatestLocalVersion()

#返回最新完整版本bigfile的路径
def GetLatestBigfilePath():
    for file in os.listdir(netRootFolder):
        if latestVersion in file:
            latestBigfilePath=os.path.join(netRootFolder,file)
            return latestBigfilePath

def GetLatetLocalBigfilePath():
    folderLocation=localRootFolder
    latestVersion=GetLatestLocalVersion()
    for file in os.listdir(folderLocation):
        if latestVersion in file:
            latestBigfilePath=os.path.join(folderLocation,file)
            return latestBigfilePath

def GetLatestNetDeployPath():
    for file in os.listdir(latestBigfileNetPath):
        if latestVersion in file:
            latestNetDeployPath=os.path.join(latestBigfileNetPath,file)
            return latestNetDeployPath

#将某个文件夹下的所有文件复制到目标目录
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

#将网络路径上的bigfile复制到本地 
def CopyBigFiles(bigfile,localfolder):
    
    folderName=FindFile(bigfile,latestVersion,"filename")
    folderPathNet=os.path.join(bigfile,folderName)
    folderPathLocal=os.path.join(localfolder,folderName)

    if not os.path.exists(folderPathLocal):
        os.makedirs(folderPathLocal)

    CopyFiles(folderPathNet,folderPathLocal)
    print(folderPathNet,folderPathLocal)
    print("Copy bigfile "+bigfile+" Done!")

#删除目录下的所有文件 
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

def DeleteAllFlies(target):
    if os.path.isfile(target):
        os.remove(target)
    else:
        DeleteFlies(target)
        if os.path.exists(target):
            DeleteEmptyFolder(target)

#删除多层空文件夹
def DeleteEmptyFolder(dir):
    if os.path.isdir(dir):
        for folder in os.listdir(dir):
            DeleteEmptyFolder(os.path.join(dir, folder))
    if not os.listdir(dir):
      os.rmdir(dir)
      print('Delete empty folder: ' + dir)

#删除除最新两个bigfile以外的其它bigfile
def DeleteOldBigFlies(targetDir):
    numArray=[]
    for file in os.listdir(targetDir):
        #filetiger_TR11_11h57_durango_C196245_A196245
        buildNum=file.split('_',4)[4]#以‘_’为标识分割4次并取第5个元素
        numArray.append(buildNum)
    if len(numArray)==0:
        print("There are currently no bigfiles in local folder")
        return
    numArray.sort()#正序排序    
    if len(numArray)>=3:#删除数组中最后两个元素
        numArray.pop()
        numArray.pop()
        for bigfile in os.listdir(targetDir):
            for i in numArray:
                if i in bigfile:
                    oldBigfilePath=os.path.join(targetDir,bigfile)
                    DeleteAllFlies(oldBigfilePath)
    else:
        print("Backup bigfiles is less than 3, skip clean")

#deploy网络上已经存在的最新版本bigfile
def CopyAndDeployLatest():
    SyncToLatest=False
    if latestLocalVersion==latestVersion:
        "You already get the latest version to local, deploy it from local"
        SyncToLatest=True   
            
    if SyncToLatest == False:
        DeleteOldBigFlies(localRootFolder)
        CopyBigFiles(latestBigfileNetPath,localRootFolder)
        latestBigfileLocalPath=GetLatetLocalBigfilePath()
            
    UninstallXboxGame(gametitle)
    DeployXboxGame(gametitle,latestBigfileLocalPath)
    Delay(5,"Game launch")
    LaunchGame(appid)

#deploy本地已经备份的最新版本bigfile
def DeployGameFromLocal():
    global latestBigfileLocalPath
    print("Now is deploying game from local file")
    UninstallXboxGame(gametitle)
    DeployXboxGame(gametitle,latestBigfileLocalPath)
    LaunchGame(appid)

#直接从buildmachine通过网络deploy
def DeployGameFromNet():
    print("Current latest version in build machine is "+latestVersion+".")
    print("Now is deploying latest file from build machine")
    GetLatestBigfilePath()

    UninstallXboxGame(gametitle)
    DeployXboxGame(gametitle,GetLatestNetDeployPath())
    LaunchGame(appid)

#检测本地和BuilldMachine上的bigfile版本
def CheckVersion():
    print("Current latest version in build machine is "+latestVersion+".\n")
    print("Current latest version in local bigfile folder is "+latestLocalVersion+".\n")

    if latestVersion==latestLocalVersion:
        print("Your local bigfile is the latest version")
    elif latestVersion=="None":
        print("Connect to server faild, check later")
    else:
        print("There is new version in build machine")

def Select_NoGUI(online):

    CheckLocalPath(localRootFolder)
    latestLocalVersion=GetLatestLocalVersion()
    latestBigfileLocalPath=GetLatetLocalBigfilePath()
    Info()

    flag = True
    while (flag):
        print("\nPlease input:")
        userInput=input()
        if userInput=="0":
            flag=False
            #os._exit()

        elif userInput=="1":
            if online:
                CopyAndDeployLatest()
            else:
                print("Faild to connect build machine")
                online=CheckConnection(netRootFolder)

        elif userInput=="2":
            DeployGameFromLocal()

        elif userInput=="3":
            if online:
                DeployGameFromNet()
            else:
                online=CheckConnection(netRootFolder)

        elif userInput=="4":
            if online:
                CheckVersion()
            else:
                print("Faild to connect build machine")
                online=CheckConnection(netRootFolder)            

        elif userInput=="5":
            CheckLocalPath(localRootFolder)
            DeleteBackupBigfiles()

        elif userInput=="6":
            CheckConnection(netRootFolder)
            
        #Debug用
        elif userInput=="9":
            Delay(5,"Game launch")
            Delay(900,"Reconnect")
            testPath=r"E:\Bigfiletest"
            testNetPath=r"\\10.0.0.68\Common\Projects\Tomb Raider\TA"
            latestVersion="test"
        else:
            print("Please input correct command\n")
            Info()



    