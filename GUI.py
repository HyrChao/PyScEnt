# encoding: utf-8
#2017/11/23 Chao 

import tkinter
import tkinter.filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import threading
from threading import Thread
from queue import Queue
import Tools as tool
import sys
import os

#class StdRedirector(object):

#    def __init__(self, text_widget):
#        self.text_space = text_widget

#    def write(self, string):
#        self.text_space.config(state=Tkinter.NORMAL)
#        self.text_space.insert("end", string)
#        self.text_space.see("end")
#        self.text_space.config(state=Tkinter.DISABLED)

class MainGUI(Thread):

    def  __init__(self,title="Tr11 Virtuos tools",width=290, height=250):
        
        self.window = tkinter.Tk(className=title)

        self.fm1=tkinter.LabelFrame(self.window,text="Tools")
        self.fm2=tkinter.Frame(self.window)

        self.fm1.pack(side='left',padx=5)
        self.fm2.pack(side='left')
        #self.fm1.grid(row = 0,column = 0,padx = 5,pady = 5)
        #self.fm1.grid(row = 0,column = 1,padx = 5,pady = 5)

        self.ico = "icon.ico"
        try:
            self.window.iconbitmap(self.ico)
        except Exception:
            self.ico=None
        
        self.w = width  
        self.h = height

        #Redirect output
        #sys.stdout = StdRedirector(text_box)
        #sys.stderr = StdRedirector(text_box)

        #Frame1
        self.button1 = tkinter.Button(self.fm1,text = "AutoSetup",width = 10,height = 5)  
        self.button2 = tkinter.Button(self.fm1,text = "Bigfile\nManager",width = 10,height = 5)  
        self.button3 = tkinter.Button(self.fm1,text = "Delete\nGenerateData",width = 10,height = 5)  
        self.button4 = tkinter.Button(self.fm1,text = "FixMyDurango",width = 10,height = 5)
        self.button5 = tkinter.Button(self.fm1,text = "CreateLink\nTool",width = 10,height = 5)
        self.button6 = tkinter.Button(self.fm1,text = "Quit",width = 10,height = 5)     
        
        #Grid for frame 1
        self.button1.grid(row = 0,column = 0,padx = 5,pady = 5)  
        self.button2.grid(row = 0,column = 1,padx = 5,pady = 5)  
        self.button3.grid(row = 0,column = 2,padx = 5,pady = 5)  
        self.button4.grid(row = 1,column = 0,padx = 5,pady = 5)
        self.button5.grid(row = 1,column = 1,padx = 5,pady = 5)
        self.button6.grid(row = 1,column = 2,padx = 5,pady = 5)
        
        #Bind button event
        self.button1.bind("<ButtonRelease-1>",self.AutoSetup)  
        self.button2.bind("<ButtonRelease-1>",self.BigfileManager)  
        self.button3.bind("<ButtonRelease-1>",self.DeleteGenerateData)  
        self.button4.bind("<ButtonRelease-1>",self.FixMyDurango)
        self.button5.bind("<ButtonRelease-1>",self.CreateLink)
        self.button6.bind("<ButtonRelease-1>",self.Quit)

    def AutoSetup(self,event):
        auto=AutoSetupGUI()
        
    def BigfileManager(self,event):
        bfm=BigfileManagerGUI()

    def DeleteGenerateData(self,event):  
        gm=GenerateDataGUI()

    def FixMyDurango(self,event):  
        if tkinter.messagebox.askokcancel("FixMyDurango","This command will close your engine and restart xbox, make sure all your work saved!!"):
            th=threading.Thread(target=tool.AutoFix)
            th.setDaemon(True)
            th.start()

    def CreateLink(self,event):  
        #tkinter.messagebox.showinfo("AssetsLinkTool","Linking assets folder to E:\\, please waite...")
        slt=CreateSymbolLinkToolGUI()   
        
    def Quit(self,event):        
        Quit()

    def Center(self):  
        ws = self.window.winfo_screenwidth()  
        hs = self.window.winfo_screenheight()  
        x = int( (ws/2) - (self.w/2) )  
        y = int( (hs/2) - (self.h/2) )  
        self.window.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))

    def StartMainGUI(self):
        self.window.resizable(False, False)   #禁止修改窗口大小  
        self.Center()
        self.window.mainloop()

class GeneralSubGUI(tkinter.Toplevel):

    def __init__(self,title="GenerateDataManager",width=280, height=100):        
        #调用父类中的__init__()函数
        super().__init__()
        self.title(title)

        #图标
        self.ico = "icon.ico"
        try:
            self.iconbitmap(self.ico)
        except Exception:
            self.ico=None

        #窗口位置及大小
        self.w=width
        self.h=height
        ws = self.winfo_screenwidth()  
        hs = self.winfo_screenheight()
        x = int( (ws/2) - (self.w/2))  
        y = int( (hs/2) - (self.h/2))
        self.resizable(0,0)
        self.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))
        
class AutoSetupGUI(GeneralSubGUI):

    def __init__(self,title="AutoDeploy",width=200 , height=160):
        
        #调用父类中的__init__()函数        
        super().__init__(title,width,height)

        self.frame = tkinter.LabelFrame(self, text="Select a tool:")
        self.frame.pack(side="top", padx=10, pady=5)
        self.buttonFrame=tkinter.Frame(self)
        self.buttonFrame.pack(side="bottom", padx=10, pady=5) 

        # 创建一个下拉列表
        self.tool = tkinter.StringVar()
        toolChosen = tkinter.ttk.Combobox(self.frame, width=15, textvariable=self.tool, state='readonly')
        toolChosen['values'] = ("AssetsLinkTool","AutoDeploy","AutoCopyLatestBigfile","TestGUI","Test")     # 设置下拉列表的值
        toolChosen.grid(column=0, row=0,padx=15, pady=15)      # 设置其在界面中出现的位置  column代表列   row 代表行
        toolChosen.current(0)    # 设置下拉列表默认显示的值，0为 toolChosen['values'] 的下标值

        #self.TestButton = tkinter.Button(self.frame,text = "Test",width = 8,height = 3)
        #self.TestButton.bind("<ButtonRelease-1>",self.Test)
        #self.TestButton.grid(row = 0,column = 0,padx = 5,pady = 5)

        self.confirmButton = tkinter.Button(self.buttonFrame,text = "Start",width = 8,height = 3)
        self.confirmButton.bind("<ButtonRelease-1>",self.Confirm)
        self.confirmButton.pack(side="left",padx=10, pady=10)
        self.cancelButton = tkinter.Button(self.buttonFrame,text = "Cancel",width = 8,height = 3)
        self.cancelButton.bind("<ButtonRelease-1>",self.Cancel)
        self.cancelButton.pack(side="left",padx=10, pady=10)

        self.mainloop()

    def Test(self):
        state=os.access(r"\\10.0.0.68\Common\Projects\Tomb Raider\TA",True)
        print(state)

    def TestGUI(self):
        tGUI=TestGUI()

    def Confirm(self,event):
        currentTool=self.tool.get()
        if currentTool == "TestGUI":
            self.TestGUI()
        elif currentTool == "AssetsLinkTool":
            self.StartAssetsLinkTool()
        elif currentTool == "AutoDeploy":
            tool.AutoDeploy()
        elif currentTool == "AutoCopyLatestBigfile":
            tool.AutoCopyBigfile()
        elif currentTool == "Test":
            self.Test()

    def Cancel(self,event):
        self.destroy() 

    def StartAssetsLinkTool():
        th=threading.Thread(target=linkTool.Auto)
        th.setDaemon(True)
        th.start()

class BigfileManagerGUI(GeneralSubGUI):

    def __init__(self,title="BigfileManager",width=400, height=300):
        
        #调用父类中的__init__()函数        
        super().__init__(title,width,height)

        self.bf=tool.GetBigfileMannager(r"E:\BigFiles",r"\\10.0.0.68\Common\Projects\Tomb Raider\DaylyBigFile")

        self.leftFrame = tkinter.Frame(self)
        self.leftFrame.pack(side="left",padx=10,pady=10)
        self.stateFrame = tkinter.LabelFrame(self.leftFrame, text="Bigfile State:")
        self.stateFrame.pack(side="top", padx=0, pady=10)
        self.dirFrame = tkinter.LabelFrame(self.leftFrame, text="Change direction:")
        self.dirFrame.pack(side="top", padx=0, pady=10)
     
        self.connected = tkinter.StringVar()
        self.localVersion = tkinter.StringVar()
        self.netVersion = tkinter.StringVar()
        self.connected.set(str(self.bf.connected))
        self.localVersion.set(self.bf.localVersion)
        self.netVersion.set(self.bf.netVersion)

        tkinter.Label(self.stateFrame, text="Connection state: ").grid(column=0, row=0,padx=2, pady=0,sticky=tkinter.W)  
        tkinter.Label(self.stateFrame, text="LocalVersion: ").grid(column=0, row=1,padx=2, pady=0,sticky=tkinter.W)  
        tkinter.Label(self.stateFrame, text="NetVersion: ").grid(column=0, row=2,padx=2, pady=0,sticky=tkinter.W)  
        tkinter.Label(self.stateFrame, textvariable=self.connected).grid(column=1, row=0,padx=2, pady=0,sticky=tkinter.W)  
        tkinter.Label(self.stateFrame, textvariable=self.localVersion).grid(column=1, row=1,padx=2, pady=0,sticky=tkinter.W)
        tkinter.Label(self.stateFrame, textvariable=self.netVersion).grid(column=1, row=2,padx=2, pady=0,sticky=tkinter.W)  

        self.sourcePath = tkinter.StringVar()
        self.sourcePath.set(r"//10.0.0.68/Common/Projects/Tomb Raider/DaylyBigFile")
        tkinter.Label(self.dirFrame, text="Source Dir:").grid(column=0, row=0,padx=2, pady=2,sticky=tkinter.W)    # 添加一个标签，并将其列设置为1，行设置为0
        self.sourceTextBar = tkinter.Entry(self.dirFrame, width=27, textvariable=self.sourcePath)   # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
        self.sourceTextBar.grid(column=0, row=1, padx=5, pady=2,sticky=tkinter.W)
        self.sourceButton = tkinter.Button(self.dirFrame,text = "...",width = 2,height = 1)
        self.sourceButton.bind("<ButtonRelease-1>",self.SelectSourcePath)
        self.sourceButton.grid(column=1, row=1,padx=5, pady=2)
        tkinter.Label(self.dirFrame, text="Target Dir:").grid(column=0, row=2,padx=2, pady=2,sticky=tkinter.W)    # 添加一个标签，并将其列设置为1，行设置为0
        self.targetPath = tkinter.StringVar()
        self.targetPath.set(r"E:/BigFiles")
        self.targetTextBar = tkinter.Entry(self.dirFrame, width=27, textvariable=self.targetPath)   # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
        self.targetTextBar.grid(column=0, row=3,padx=5, pady=2, sticky=tkinter.W)
        self.targetButton = tkinter.Button(self.dirFrame,text = "...",width = 2,height = 1)
        self.targetButton.bind("<ButtonRelease-1>",self.SelectTargetPath)
        self.targetButton.grid(column=1, row=3,padx=5, pady=2)

        self.actionFrame=tkinter.LabelFrame(self, text="Acion:")
        self.actionFrame.pack(side="right", padx=10, pady=5) 

        self.copyButton = tkinter.Button(self.actionFrame,text = "CopyLatest",width = 8,height = 3)
        self.copyButton.bind("<ButtonRelease-1>",self.CopyLatest)
        self.copyButton.pack(side="top",padx=10, pady=10)  
        self.deployButton = tkinter.Button(self.actionFrame,text = "Deploy\n(dev)",width = 8,height = 3)
        self.deployButton.bind("<ButtonRelease-1>",self.Deploy)
        self.deployButton.pack(side="top",padx=10, pady=10)  
        self.cancelButton = tkinter.Button(self.actionFrame,text = "Cancel",width = 8,height = 3)
        self.cancelButton.bind("<ButtonRelease-1>",self.Cancel)
        self.cancelButton.pack(side="top",padx=10, pady=10)

        self.mainloop()
 
    def SelectSourcePath(self,event):
        #path=tkinter.filedialog.askopenfilename()
        path=tkinter.filedialog.askdirectory(title = "Select Source Path", initialdir=r"\\10.0.0.68\Common\Projects\Tomb Raider\DaylyBigFile", mustexist = True, parent = self)
        print(path)
        if os.path.isdir(path):
            self.sourcePath.set(path)
            self.bf.SetNetDir(path)
            self.connected.set(str(self.bf.connected))
            self.localVersion.set(self.bf.localVersion)
            self.netVersion.set(self.bf.netVersion)


    def SelectTargetPath(self,event):
        #tPath=tkinter.filedialog.askopenfilename()
        path=tkinter.filedialog.askdirectory(title = "Select Target Path", initialdir=r"E:\\", mustexist = True, parent = self)
        print(path)
        if os.path.isdir(path):
            self.targetPath.set(path)
            self.bf.SetLocalDir(path)
            self.connected.set(str(self.bf.connected))
            self.localVersion.set(self.bf.localVersion)
            self.netVersion.set(self.bf.netVersion)

    def CopyLatest(self,event):
        self.bf.PrintState()
        self.bf.CopyLatesstToLocal()
        
    def Deploy(self,event):
        pass

    def Cancel(self,event):
        self.destroy() 

class GenerateDataGUI(GeneralSubGUI):

    #mode=0  #0 == Wwise #1 == Simplygon #2 == Filename
    # 定义几个模式的全局变量
    mode = ["Wwise", "Simplygon", "Filename"]
    currentMode=None
    def __init__(self,title="GenerateData Manager",width=200, height=180):
        
        #调用父类中的__init__()函数        
        super().__init__(title,width,height)

        self.frame = tkinter.LabelFrame(self, text="Delete GenerateData By:")
        self.frame.pack(side="top", padx=5, pady=5)
        self.buttonFrame=tkinter.Frame(self)
        self.buttonFrame.pack(side="bottom", padx=10, pady=5)
         
        self.confirmButton = tkinter.Button(self.buttonFrame,text = "Confirm",width = 8,height = 2)
        self.confirmButton.bind("<ButtonRelease-1>",self.Confirm)
        self.cancelButton = tkinter.Button(self.buttonFrame,text = "Cancel",width = 8,height = 2)
        self.cancelButton.bind("<ButtonRelease-1>",self.Cancel)
        self.confirmButton.pack(side="left",padx=10, pady=10)  
        self.cancelButton.pack(side="left",padx=10, pady=10)  
        

        radVar = tkinter.IntVar()    # 通过tk.IntVar() 获取单选按钮value参数对应的值
        radVar.set(99)

        self.fileNameToDelete = tkinter.StringVar()
        self.textBar = tkinter.Entry(self.frame, width=8, textvariable=self.fileNameToDelete)   # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
        self.textBar.grid(column=1, row=2, sticky=tkinter.W)
        self.textBar.configure(state='disabled')  #默认关闭文本框

        def RadCall():
            radSel = radVar.get()
            if radSel == 0:
                self.currentMode=self.mode[0]
                print(self.currentMode)
                self.textBar.configure(state='disabled')  #关闭文本框

            elif radSel == 1:
                self.currentMode=self.mode[1]
                print(self.currentMode)
                self.textBar.configure(state='disabled')  #关闭文本框

            elif radSel == 2:
                self.currentMode=self.mode[2]
                print(self.currentMode)
                self.textBar.configure(state='normal')  #开启文本框

                #self.fileNameToDelete="ce_crank"

        for mod in range(3):
            # curRad = 'rad' + str(col)
            curRad = tkinter.Radiobutton(self.frame, text=self.mode[mod], variable=radVar, value=mod, command=RadCall)    # 当该单选按钮被点击时，会触发参数command对应的函数
            curRad.grid(column=0, row=mod, sticky=tkinter.W)     # 参数sticky对应的值参考复选框的解释
       
        self.mainloop()

    def Confirm(self,event):

        if self.currentMode==None:
            tkinter.messagebox.showinfo("Invalid Data","Please select a mode")  
        elif self.currentMode!="Filename":
            tool.DeleteGenerateData(self.currentMode)
        else:
            inputFileName=self.fileNameToDelete.get()
            print(inputFileName)
            tool.DeleteGenerateData(self.currentMode,inputFileName)

    def Cancel(self,event):
        self.destroy()

class CreateSymbolLinkToolGUI(GeneralSubGUI):
    
    def __init__(self,title="CreateSymbolLinkTool",width=250, height=180):
        targetPath=None
        sourcePath=None
        #调用父类中的__init__()函数        
        super().__init__(title,width,height)

        self.frame = tkinter.LabelFrame(self, text="Select path:")
        self.frame.pack(side="top", padx=10, pady=10)
        self.buttonFrame=tkinter.Frame(self)
        self.buttonFrame.pack(side="bottom", padx=10, pady=10)
        
        self.sourcePath = tkinter.StringVar()
        self.sourcePath.set("Select source path...")
        self.sourceTextBar = tkinter.Entry(self.frame, width=25, textvariable=self.sourcePath)   # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
        self.sourceTextBar.grid(column=0, row=0, padx=5, pady=2,sticky=tkinter.W)
        self.sourceButton = tkinter.Button(self.frame,text = "...",width = 2,height = 1)
        self.sourceButton.bind("<ButtonRelease-1>",self.SelectSourcePath)
        self.sourceButton.grid(column=1, row=0,padx=5, pady=2)

        self.targetPath = tkinter.StringVar()
        self.targetPath.set("Select target path...")
        self.targetTextBar = tkinter.Entry(self.frame, width=25, textvariable=self.targetPath)   # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
        self.targetTextBar.grid(column=0, row=1,padx=5, pady=2, sticky=tkinter.W)
        self.targetButton = tkinter.Button(self.frame,text = "...",width = 2,height = 1)
        self.targetButton.bind("<ButtonRelease-1>",self.SelectTargetPath)
        self.targetButton.grid(column=1, row=1,padx=5, pady=2)

        self.confirmButton = tkinter.Button(self.buttonFrame,text = "Create",width = 8,height = 3)
        self.confirmButton.bind("<ButtonRelease-1>",self.Confirm)
        self.confirmButton.pack(side="left",padx=10, pady=10)  
        self.cancelButton = tkinter.Button(self.buttonFrame,text = "Cancel",width = 8,height = 3)
        self.cancelButton.bind("<ButtonRelease-1>",self.Cancel)
        self.cancelButton.pack(side="left",padx=10, pady=10)

        self.mainloop()

    def SelectSourcePath(self,event):
        #path=tkinter.filedialog.askopenfilename()
        path=tkinter.filedialog.askdirectory(title = "Select Source Path", initialdir=r"D:\tr11\tr11_dev", mustexist = True, parent = self)
        print(path)
        if os.path.isdir(path):
            self.sourcePath.set(path)

    def SelectTargetPath(self,event):
        #tPath=tkinter.filedialog.askopenfilename()
        path=tkinter.filedialog.askdirectory(title = "Select Target Path", initialdir="E:\\", mustexist = True, parent = self)
        print(path)
        if os.path.isdir(path):
            self.targetPath.set(path)

    def Confirm(self,event):
        srcPath=self.sourcePath.get()
        tarPath=self.targetPath.get()
        if os.path.isdir(srcPath) and os.path.isdir(tarPath):
            tool.SetupLink(srcPath,tarPath)
        else:
            messagebox.showinfo("Warning","Path invaild!")

    def Cancel(self,event):
        self.destroy() 

def Quit():
    sys.exit()
    
def StartGUI():
    mainGUI=MainGUI()
    mainGUI.StartMainGUI()

if  __name__ =="__main__":
    StartGUI()
        
class TestGUI(GeneralSubGUI):

    def __init__(self,title="GenerateData Manager",width=350, height=300):
        
        #调用父类中的__init__()函数
        super().__init__(title,width,height)        
        
        # 创建一个容器,
        fm1 = tkinter.LabelFrame(self, text="Test Python ")     # 创建一个容器，其父容器为win
        fm1.grid(column=0, row=0, padx=10, pady=10)       # padx  pady   该容器外围需要留出的空余空间
        aLabel = tkinter.Label(fm1, text="A Label")

        tkinter.Label(fm1, text="Chooes a number").grid(column=1, row=0)    # 添加一个标签，并将其列设置为1，行设置为0
        tkinter.Label(fm1, text="Enter a name:").grid(column=0, row=0, sticky='W')      # 设置其在界面中出现的位置  column代表列   row 代表行

        # 按钮
        action = tkinter.Button(fm1, text="Click Me!", command=self.ClickMe)     # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
        action.grid(column=2, row=1)    # 设置其在界面中出现的位置  column代表列   row 代表行

        # 文本框
        name = tkinter.StringVar()     # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
        nameEntered = tkinter.Entry(fm1, width=12, textvariable=name)   # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
        nameEntered.grid(column=0, row=1, sticky=tkinter.W)       # 设置其在界面中出现的位置  column代表列   row 代表行
        nameEntered.focus()     # 当程序运行时,光标默认会出现在该文本框中

        # 创建一个下拉列表
        number = tkinter.StringVar()
        numberChosen = tkinter.ttk.Combobox(fm1, width=12, textvariable=number, state='readonly')
        numberChosen['values'] = (1, 2, 4, 42, 100)     # 设置下拉列表的值
        numberChosen.grid(column=1, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
        numberChosen.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

        # 复选框
        chVarDis = tkinter.IntVar()   # 用来获取复选框是否被勾选，通过chVarDis.get()来获取其的状态,其状态值为int类型 勾选为1  未勾选为0
        check1 = tkinter.Checkbutton(fm1, text="Disabled", variable=chVarDis, state='disabled')    # text为该复选框后面显示的名称, variable将该复选框的状态赋值给一个变量，当state='disabled'时，该复选框为灰色，不能点的状态
        check1.select()     # 该复选框是否勾选,select为勾选, deselect为不勾选
        check1.grid(column=0, row=4, sticky=tkinter.W)       # sticky=tk.W  当该列中其他行或该行中的其他列的某一个功能拉长这列的宽度或高度时，设定该值可以保证本行保持左对齐，N：北/上对齐  S：南/下对齐  W：西/左对齐  E：东/右对齐

        chvarUn = tkinter.IntVar()
        check2 = tkinter.Checkbutton(fm1, text="UnChecked", variable=chvarUn)
        check2.deselect()
        check2.grid(column=1, row=4, sticky=tkinter.W)

        chvarEn = tkinter.IntVar()
        check3 = tkinter.Checkbutton(fm1, text="Enabled", variable=chvarEn)
        check3.select()
        check3.grid(column=2, row=4, sticky=tkinter.W)

        # 单选按钮

        # 定义几个颜色的全局变量
        colors = ["Blue", "Gold", "Red"]
        radVar = tkinter.IntVar()    # 通过tk.IntVar() 获取单选按钮value参数对应的值
        radVar.set(99)
        for col in range(3):
            # curRad = 'rad' + str(col)
          curRad = tkinter.Radiobutton(fm1, text=colors[col], variable=radVar, value=col, command=self.RadCall)    # 当该单选按钮被点击时，会触发参数command对应的函数
          curRad.grid(column=col, row=5, sticky=tkinter.W)     # 参数sticky对应的值参考复选框的解释

        # 滚动文本框
        scrolW = 30 # 设置文本框的长度
        scrolH = 3 # 设置文本框的高度

        # wrap=tk.WORD   这个值表示在行的末尾如果有一个单词跨行，会将该单词放到下一行显示,比如输入hello，he在第一行的行尾,llo在第二行的行首, 这时如果wrap=tk.WORD，则表示会将 hello 这个单词挪到下一行行首显示, wrap默认的值为tk.CHAR
        scr = tkinter.scrolledtext.ScrolledText(fm1, width=scrolW, height=scrolH, wrap=tkinter.WORD)     
        scr.grid(column=0, columnspan=3)        # columnspan 个人理解是将3列合并成一列   也可以通过 sticky=tk.W  来控制该文本框的对齐方式

        self.mainloop()      # 当调用mainloop()时,窗口才会显示出来
            # button被点击之后会被执行

    def ClickMe():   # 当acction被点击时,该函数则生效
        action.configure(text='Hello ' + name.get() + ' ' + numberChosen.get())     # 设置button显示的内容
        print ('check3 is %s %s' % (type(chvarEn.get()), chvarEn.get()))

    # 单选按钮回调函数,就是当单选按钮被点击会执行该函数
    def RadCall():
        radSel = radVar.get()
        if radSel == 0:
            self.configure(background=colors[0])      # 设置整个界面的背景颜色
            print(radVar.get())
        elif radSel == 1:
            self.configure(background=colors[1])
        elif radSel == 2:
            self.configure(background=colors[2])
#class Application(Thread):  

#    def  __init__(self):
#        mainGUI=MainGUI()
#        mainGUI.StartMainGUI()       



#def save(self):
#    self.button0.config(relief=SUNKEN)
#    # if you also want to disable it do:
#    # self.button0.config(state=tk.DISABLED)
#    #...

#def stop(self):
#    self.button0.config(relief=RAISED)
#    # if it was disabled above, then here do:
#    # self.button0.config(state=tk.ACTIVE)
#    #...