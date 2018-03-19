# encoding: utf-8
#2018/01/29 Chao 

import os
import os.path
import shutil
import Core as cr
import sys


class Bigfile(object):

    localRoot=None
    netRoot=None
    
    netVersion=None
    netBigfile=None
    netBigfileName=None
    netDeployfile=None
    localVersion=None
    localBigfile=None
    localBigfileName=None
    localDeplyfile=None
    connected=False

    def __init__(self,localRootFolder=r"E:\BigFiles",netRootFolder=r"\\CNSHAW1694\ShareFolder\HourlyBigfile"):

        self.localRoot=localRootFolder
        self.netRoot=netRootFolder
        self.InitialLocalPath()
        self.CleanLocal()
        self.CheckConnection()
        self.RefreshState()
        
        self.PrintState()

    def AchieveLocalBigfile(self,reverse=False):
        '''
        default:reverse=False
        True:Get oldest local version
        False:Get latest local version
        '''
        localDirList=os.listdir(self.localRoot)
        bigfileList=[]
        for folder in localDirList:
            if "BF_TR11_" in folder:
                bigfileList.append(folder)
        #初始化二维数组
        bigfileArray=[]
        for file in bigfileList:
            #BF_TR11_13h58_durango_C196744_A196744
            version=file.split('_',4)[4]#以‘_’为标识分割4次并取第5个元素
            bigfile = []
            bigfile.append(version)
            bigfile.append(file)
            bigfileArray.append(bigfile)
        if len(bigfileArray)==0:
            print("There are currently no bigfiles in local")
            return None
        if reverse is False:
            bigfileArray.sort(reverse=True)
            return bigfileArray[0]
        else:
            bigfileArray.sort()
            return bigfileArray[0]   
        
    def AchieveNetBigfile(self,reverse=False):
        '''
        default:reverse=False
        True:Get oldest local version
        False:Get latest local version
        '''
        if self.CheckConnection:
            netDirList=os.listdir(self.netRoot)
            bigfileList=[]
            for folder in netDirList:
                if "BF_TR11_" in folder:
                    bigfileList.append(folder)
            #初始化二维数组
            bigfileArray=[]
            for file in bigfileList:
                #BF_TR11_13h58_durango_C196744_A196744
                version=file.split('_',4)[4]#以‘_’为标识分割4次并取第5个元素
                bigfile = []
                bigfile.append(version)
                bigfile.append(file)
                bigfileArray.append(bigfile)
            if len(bigfileArray)==0:
                print("There are currently no bigfiles in build machine")
                return None
            if reverse is False:
                bigfileArray.sort(reverse=True)
                if self.CheckBigfileComplement(os.path.join(self.netRoot,bigfileArray[0][1])):
                    return bigfileArray[0]
                else:
                    if len(bigfileArray) > 1:
                        return bigfileArray[1]
                    else:
                        print ("Current bigfile is still building in server, pass copy")
                        return None
            else:
                bigfileArray.sort()
                return bigfileArray[0]
        else:
            return None 
    
    def AutoDeploy(self):
        self.CopyLatesstToLocal()
        self.DeployLocalLatest()
        self.CleanLocal()

    def CheckConnection(self):
        if os.access(self.netRoot,True):
            print("Server accessable")
            self.connected=True
            return True
        else:
            print("Server access failed")
            self.connected=False
            return False  

    def InitialLocalPath(self):
        #localPathUnix=self.localRoot.replace("\\","/")
        if not os.path.exists(self.localRoot):
            os.makedirs(self.localRoot)

    def CopyLatesstToLocal(self):
        if self.connected:
            versionNumLocal=self.GetLocalVersionNumber()
            versionNumNet=self.GetNetVersionNumber()
            if self.netBigfile is not None:
               if versionNumLocal is None or versionNumNet > versionNumLocal:
                    cr.CopyFolder(self.netBigfile,self.localRoot)
                    self.RefreshLocal()
                    self.CleanLocal()
                    print("Copy lateat version %s success"%self.localVersion)
               else:
                    print("Net version is older than local")
            else:
                print("No bigfiles found in server")
        elif self.Reconnect():
            self.CopyLatesstToLocal()
            
    def CleanLocal(self):
        bigfileMark="BF_TR11_"
        dirlist=os.listdir(self.localRoot)
        virsionArray=[]
        for dir in dirlist:
            filePath=os.path.join(self.localRoot,dir)
            if bigfileMark in dir:
                if not self.CheckBigfileComplement(filePath):
                    cr.Delete(filePath)
                    print("Delete imcomplete bigfiles success")
                else:
                    version=dir.split('_',4)[4]
                    virsionArray.append(version)                   
            else:
                cr.Delete(filePath)
                print("Delete extra local files success")
        virsionArray.sort()
        if len(virsionArray) > 3:
            virsionArray=virsionArray[:-3]  #slice 去除列表后三位
            for virsion in virsionArray:
                for dir in dirlist:
                    if virsion in dir:
                        oldBigfilePath=os.path.join(self.localRoot,dir)
                        cr.Delete(oldBigfilePath)
        else:
            pass
                
    #def CheckBuildComplement(self,bigfile=None):
    #    completeMarkFile="Changelists.txt"
    #    if bigfile is not None:
    #        for file in os.listdir(bigfile):
    #            if completeMarkFile in file:
    #                return True
    #        return False                                           
    #    else:
    #        for file in os.listdir(self.netBigfile):
    #            if completeMarkFile in file:
    #                return True                
    #        return False

    def CheckBigfileComplement(self,bigfile):
        IDFiles="IDFiles"
        if bigfile is not None:
                for file in os.listdir(bigfile):
                    if IDFiles in file:
                        return True
        return False                                           

    #def CheckBigfileComplement(self,bigfile=None):
    #    completeMarkFile="TR11.exe"
    #    if bigfile is not None:
    #        for dir in os.listdir(bigfile):
    #            deployPath=os.path.join(bigfile,dir)
    #            if os.path.isdir(deployPath):
    #                filelist=os.listdir(deployPath)
    #                for file in filelist:
    #                    if completeMarkFile in file:
    #                        return True
    #        return False
    #    else:
    #        for file in os.listdir(self.netBigfile):
    #            if completeMarkFile in file:
    #                return True                
    #        return False

    def SetNetDir(self,dir):
        if os.path.isdir(dir):
            self.netRoot=dir
            self.CheckConnection()
            self.RefreshNet()
            return True
        else:
            return False

    def SetLocalDir(self,dir):
        vessel=self.localRoot
        self.localRoot=dir
        self.InitialLocalPath()
        if os.path.isdir(dir):
            self.RefreshLocal()
            return True
        else:
            self.localRoot=vessel
            return False

    def DeployLocalLatest(self):
        if self.localDeplyfile is not None:
            self.CheckBigfileComplement(self.localBigfile)
            UninstallGame()
            DeployGame(self.localDeplyfile)
            LaunchGame()

    def GetLocalVersionNumber(self):
        if self.localBigfile is not None:
            versionNum=int((str(self.localVersion).split('_',1)[0])[1:])
            return versionNum
        else:
            return None
    def GetNetVersionNumber(self):
        if self.netBigfile is not None:
            versionNum=int((str(self.netVersion).split('_',1)[0])[1:])
            return versionNum
        else:
            return None

    def GetLocalVersion(self):
        return self.localVersion

    def GetNetVersion(self):
        return self.netVersion

    def GetLocalBigfile(self):
        return self.localBigfile

    def GetNetBigfile(self):
        return self.netBigfile

    def GetLocalDeployfile(self):
        return self.localDeplyfile

    def GetNetDeployfile(self):
        return self.netDeployfile

    def GetConnectionState(self):
        return self.connected

    def Reconnect(self):
        if self.connected:
            self.RefreshState()
            return True
        else:
            cr.Delay(600)
            if not self.CheckConnection():
                self.Reconnect()
            
    def RefreshState(self):
            self.RefreshLocal()
            self.RefreshNet()      

    def RefreshLocal(self):
        latestLocalBigfile=self.AchieveLocalBigfile()
        if latestLocalBigfile is not None:
            self.localVersion=latestLocalBigfile[0]
            self.localBigfileName=latestLocalBigfile[1]
            self.localBigfile=os.path.join(self.localRoot,self.localBigfileName)
            for file in os.listdir(self.localBigfile):
                mark="filetiger_"
                if mark in file:
                    self.localDeplyfile=os.path.join(self.localBigfile,file)
                    break
        else:
            self.localVersion=None
            self.localBigfile=None
            self.localBigfileName=None

    def RefreshNet(self):
        latestNetBigfile=self.AchieveNetBigfile()
        if latestNetBigfile is not None:
            self.netVersion=latestNetBigfile[0]
            self.netBigfileName=latestNetBigfile[1]
            self.netBigfile=os.path.join(self.netRoot,self.netBigfileName)
            for file in os.listdir(self.netBigfile):
                mark="filetiger_"
                if mark in file:
                    self.netDeployfile=os.path.join(self.netBigfile,file)
                    break
        else:
            self.netVersion=None
            self.netBigfile=None
            self.netBigfileName=None
    
    def PrintState(self):
        print("Connection state: %s"%self.connected)
        print("LocalVersion: %s"%self.localVersion)
        print("LocalBigfile: %s"%self.localBigfile)
        print("LocalDeployfile: %s"%self.localDeplyfile)
        print("NetVersion: %s"%self.netVersion)
        print("NetBigfile: %s"%self.netBigfile)
        print("NetDeployFile: %s"%self.netDeployfile)

def UninstallGame(gametitle="TR11OUTSOURCE_1.0.0.1_x64__ywaz7tst186jr"):
    xdkpath=r"C:\Program Files (x86)\Microsoft Durango XDK\bin"    
    print("Uninstalling old game version")
    cmd="xbapp uninstall %s"%gametitle
    #os.system("cd "+xdkpath)
    os.chdir(xdkpath)
    uninstallResault=os.popen(cmd)
    print(uninstallResault)

def DeployGame(deployFile):
    if deployFile is not None:
        xdkpath=r"C:\Program Files (x86)\Microsoft Durango XDK\bin"
        gametitle="TR11OUTSOURCE_1.0.0.1_x64__ywaz7tst186jr"
        appid="TR11OUTSOURCE_ywaz7tst186jr!TR11.App"
        #@echo Deploying tr11, please wait...
        #xbapp deploy E:\filetiger_TR11_18h09_durango_C194642_A194642
        print("Installing new game version,please wait...")
        os.chdir(xdkpath)
        cmd="xbapp deploy %s"%deployFile
        print(cmd)
        deployResault=os.popen(cmd)
        print(deployResault)
        if deployResault=="The operation completed successfully.":
            print("The operation completed successfully.")
            return True    
    else:
        return False

def LaunchGame(appid="TR11OUTSOURCE_ywaz7tst186jr!TR11.App"):
    xdkpath=r"C:\Program Files (x86)\Microsoft Durango XDK\bin"
    gametitle="TR11OUTSOURCE_1.0.0.1_x64__ywaz7tst186jr"
    print("launching game...")
    os.chdir(xdkpath)
    cmd="xbapp launch %s"%appid
    os.system(cmd)

def Info():
    print("\n")
    print("======================================================================================================\n")
    print("Copy latest version to local and deploy                 (1)   |        Copy latest bigfile to local(2)\n")
    print("Deploy from local                                       (3)   |                                       \n")
    print("                                                                                             Quit(0)\n")
    print("======================================================================================================\n")          
    print("\n")

if  __name__ =="__main__":

    if len(sys.argv) >=2:
        bf=Bigfile()
        print("Current mode:"+sys.argv[1])
        if sys.argv[1]=="-auto":            
            bf.AutoDeploy()

        elif sys.argv[1]=="-copy":
            bf.CopyLatesstToLocal()

        elif sys.argv[1]=="-server":
            bf.SetLocalDir(r"\\10.0.0.68\Common\Projects\Tomb Raider\DailyBigFile")
            bf.CopyLatesstToLocal()

    else:
        Info()
        bf=Bigfile()
        flag = True
        while (flag):
            print("\nPlease input:")
            userInput=input()
            if userInput=="0":
                flag=False
            elif userInput=="1":
                bf.AutoDeploy()
            elif userInput=="2":
                bf.CopyLatesstToLocal()
            elif userInput=="3":
                bf.DeployLocalLatest()
            else:
                print("Please input correct command\n")
                Info()
    #Info()
    #flag = True
    #bf=Bigfile()
    #while (flag):
    #    print("\nPlease input:")
    #    userInput=input()
    #    if userInput=="0":
    #        flag=False
    #    elif userInput=="1":
    #        bf.AutoDeploy()
    #    elif userInput=="2":
    #        bf.CopyLatesstToLocal()
    #    elif userInput=="3":
    #        bf.DeployLocalLatest()
    #    else:
    #        print("Please input correct command\n")
    #        Info()

        
