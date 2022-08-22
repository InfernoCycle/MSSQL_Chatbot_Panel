import os
import pathlib
import shutil
import subprocess
import tkinter as tk
from tkinter import CENTER, END, LEFT, NSEW, ttk
from tkinter import simpledialog
from tkinter import filedialog
import pyodbc
import json
import sys

print(os.path.expanduser("~"))
print(__file__)
print(os.listdir("./"))
application_path = ""
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

print(application_path, 9)
class App():
    def __init__(self, parent) -> None:
        self.btnWidth = 10
        self.btnFont = ("Times New Roman", 12, "bold")
        self.btnFG = ""
        self.btnDisCol = "gray"
        
        self.Server = ""
        self.Database = ""
        self.Table = ""
        self.Username = ""
        self.Password = ""
        
        drive = str(pathlib.Path.home())[0:2]
        self.destination = drive + "/Program Files/HNBAdmin"
        
        #OG sizes 400, 289
        self.master = parent
        self.master.title("Chatbot Installer")
        self.master.geometry("400x289")
        self.master.maxsize(400, 289)
        self.master.minsize(400, 289)
        self.master.grid_columnconfigure([0,1], weight=1)
        self.master.grid_rowconfigure([0,1,2], weight=1)
        
        self.agreement()
    
    def agreement(self):
        for i in self.master.winfo_children():
            i.destroy()
            
        def changeState():
            if(intVar.get() == 1):
                Next.config(state="normal", background="white")
            elif(intVar.get() == 0):
                Next.config(state="disabled", background="lightgray")
                
        Panel = tk.Frame(self.master)
        Panel.grid_columnconfigure([0], weight=1)
        Panel.grid_rowconfigure([0,1], weight=1)
        
        intVar = tk.IntVar(Panel, value=0)
        
        Top = tk.Frame(Panel)
        Top.grid_columnconfigure([0], weight=1)
        Top.grid_rowconfigure([0,1,2], weight=1)
        Title = tk.Label(Top, text="Terms and Agreements", font=("Times New Roman", 15, "bold"))
        Text = tk.Text(Top, height=10)
        Text.insert("1.0", "In agreeing with the terms and agreement you acknowledge that Carlin Rogers is the soul creator and owner of this installer. Feel free to use this service at your own caution. Please be sure that this application was sent by a trustworthy source.")
        Text.config(state="disabled")
        Check = ttk.Checkbutton(Top, command=lambda:changeState(), text="Agree and Continue", variable=intVar)
        Title.grid(row=0, column=0, pady=5)
        Text.grid(row=1, column=0, padx=20)
        Check.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        Pages = tk.Frame(Panel)
        Pages.grid_columnconfigure([0,1], weight=1)
        Pages.grid_rowconfigure([0,1], weight=1)
        Back = tk.Button(Pages, text="Back", width=self.btnWidth, font=self.btnFont)
        Back.config(state="disabled", background="lightgray")
        Next = tk.Button(Pages, text="Next", width=self.btnWidth, font=self.btnFont, command=lambda:self.databaseSetting())
        Next.config(state="disabled", background="lightgray")
        Back.grid(row=0, column=0, sticky="e", pady=5, padx=4)
        Next.grid(row=0, column=1, sticky="e", pady=5, padx=4)
        
        #Top.grid(row=0, column=0)
        Top.grid(row=0, column=0)
        #Pages.grid(row=1, column=0, sticky="e", padx=20)
        Pages.grid(row=1, column=0, padx=20, pady=5)
        Panel.grid(row=0, column=0)
        
    def databaseSetting(self):
        for i in self.master.winfo_children():
            i.destroy()
        
        def updateVariableAndPage():
            self.Server = ServerText.get("1.0", END).strip()
            self.Database = DatabaseText.get("1.0", END).strip()
            self.Table = TableText.get("1.0", END).strip()
            self.Username = UsernameText.get("1.0", END).strip()
            self.Password = PasswordText.get("1.0", END).strip()
            
            self.testConnection()
        
        Panel = tk.Frame(self.master)
        Panel.grid_rowconfigure([0,1,2,3,4,5,6,7,8,9,10], weight=1)
        Panel.grid_columnconfigure([0,1], weight=1)
        
        yesStr = tk.IntVar(Panel, value=0)
        noStr = tk.IntVar(Panel, value=0)
        
        Lbl = tk.Label(Panel,justify=CENTER, wraplength=400, text="Enter SQL Credentials below (Note: settings can be changed after program is installed): ")
        #yes = ttk.Checkbutton(Panel, textvariable=yesStr, text="Yes (This will create a new database (only supports azure sql and mssql)", command=lambda:ShowYes())
        #no = ttk.Checkbutton(Panel, textvariable=noStr, text="No ", command=lambda:ShowNo())
        
        ServerLabel = tk.Label(Panel, text="Server:")
        ServerText = tk.Text(Panel, height=1)
        ServerText.insert("1.0", self.Server)
        
        DatabaseLabel = tk.Label(Panel, text="Database:")
        DatabaseText = tk.Text(Panel, height=1)
        DatabaseText.insert("1.0", self.Database)
        
        TableLabel = tk.Label(Panel, text="Table:")
        TableText = tk.Text(Panel, height=1)
        TableText.insert("1.0", self.Table)
        
        UsernameLabel = tk.Label(Panel, text="Username:")
        UsernameText = tk.Text(Panel, height=1)
        UsernameText.insert("1.0", self.Username)
        
        PasswordLabel = tk.Label(Panel, text="Password:")
        PasswordText = tk.Text(Panel, height=1)
        PasswordText.insert("1.0", self.Password)
        
        Lbl.grid(row=0, column=0, sticky="w")
        #yes.grid(row=1, column=0, sticky="w")
        #no.grid(row=2, column=0, sticky="w")
        ServerLabel.grid(row=1, column=0, padx=20)
        ServerText.grid(row=2, column=0, padx=20)
        
        DatabaseLabel.grid(row=3, column=0, padx=20)
        DatabaseText.grid(row=4, column=0, padx=20)
        
        TableLabel.grid(row=5, column=0, padx=20)
        TableText.grid(row=6, column=0, padx=20)
        
        UsernameLabel.grid(row=7, column=0, padx=20)
        UsernameText.grid(row=8, column=0, padx=20)
        
        PasswordLabel.grid(row=9, column=0, padx=20)
        PasswordText.grid(row=10, column=0, padx=20)
        
        Bottom = tk.Frame(Panel)
        Back = tk.Button(Bottom, text="Back", width=self.btnWidth, font=self.btnFont, command=lambda:self.agreement())
        #Back.config(state="disabled", background="lightgray")
        Next = tk.Button(Bottom, text="Next", width=self.btnWidth, font=self.btnFont, command=lambda:updateVariableAndPage())
        Back.grid(row=0, column=0, sticky="e", pady=5, padx=4)
        Next.grid(row=0, column=1, sticky="e", pady=5, padx=4)
        
        Bottom.grid(row=11, column=0)
        Panel.grid(row=0, column=0, sticky="ewns")

    def testConnection(self):
        for i in self.master.winfo_children():
            i.destroy()
        
        status = "Not Connected"
        
        try:
            cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.Server+';DATABASE='+self.Database+';UID='+self.Username+';PWD='+ self.Password)
            status = "Connected"
            cnxn.close()
        except:
            print("Not connected")
            
        Panel = tk.Frame(self.master)
        Panel.grid_rowconfigure([0,1,2,3], weight=1)
        Panel.grid_columnconfigure([0,1], weight=1)
        ConnectionLabel = tk.Label(Panel, text="Status: " + str(status))

        def getDirectory():
            directory = filedialog.askdirectory()
            #self.destination = DestinationText.get("1.0", END).strip()
            #print(self.destination)
            if(directory.strip() != ""):
                DestinationText.delete("1.0", END)
            
            DestinationText.insert("1.0", directory.strip())
            #if("HNBAdmin" not in directory.strip()):
             #   DestinationText.delete("1.0", END)
              #  DestinationText.insert("1.0", directory.strip() + "/HNBAdmin")
        
        def changePages():
            self.destination = DestinationText.get("1.0", END).strip()
            if("HNBAdmin" not in self.destination):
                self.destination += "/HNBAdmin"
            print(self.destination)
            self.install()
            
        DirectorySpace = tk.Frame(self.master)
        DirectorySpace.grid_rowconfigure([0,1,2], weight=1)
        DirectorySpace.grid_columnconfigure([0,1], weight=1)
        DestinationLabel = tk.Label(DirectorySpace, text="Choose Destination to Install: ")
        DestinationText = tk.Text(DirectorySpace, height=2, width=30)
        DestinationText.insert("1.0", self.destination)
        OpenDialog = tk.Button(DirectorySpace, text="Choose Directory", height=1, command=lambda:getDirectory())
        
        ConnectionLabel.pack()
        DestinationLabel.grid(row=0, column=0, columnspan=2)
        DestinationText.grid(padx=5, row=1, column=0)
        OpenDialog.grid(padx=20, row=1, column=1)
        
        Bottom = tk.Frame(self.master)
        Back = tk.Button(Bottom, text="Back", width=self.btnWidth, font=self.btnFont, command=lambda:self.databaseSetting())
        #Back.config(state="disabled", background="lightgray")
        Next = tk.Button(Bottom, text="Next", width=self.btnWidth, font=self.btnFont, command=lambda:changePages())
        Back.grid(row=0, column=0, sticky="e", pady=5, padx=4)
        Next.grid(row=0, column=1, sticky="e", pady=5, padx=4)
        
        Bottom.pack(side="bottom")
        Panel.pack(side=["top"], fill="both")
        DirectorySpace.pack(anchor="center", fill="both", expand=True)
    
    def install(self):
        for i in self.master.winfo_children():
            i.destroy()
            
        Top = tk.Frame(self.master)
        Top.grid_rowconfigure([0,1], weight=1)
        Label = tk.Label(Top, text="Install", font=("Times New Roman", 20, "bold"))
        Label.grid(row=0, column=0)
        
        Center = tk.Frame(self.master)
        Center.grid_rowconfigure([0,1], weight=1)
        NoteLabel = tk.Label(Center, text="Note: Settings may be changed within the app", font=("Times New Roman", 13, "bold"))
        shortcutVar = tk.IntVar(Center, value=0)
        Shortcut = ttk.Checkbutton(Center, variable=shortcutVar, text="Include Shortcut")
        NoteLabel.grid(row=0, column=0)
        Shortcut.grid(row=1, column=0)
        
        Bottom = tk.Frame(self.master)
        
        def Install():
            #path = self.destination + "/settings.json"
            directory = os.path.expanduser("~") + "/AppData/Roaming/HNBAdmin/"
            file = directory + "settings.json"
            #file = ""
            print(file)

            if(not (pathlib.Path(file).is_file())):
                #directory = os.path.join(os.path.dirname(__file__), "admin")
                try:
                    os.mkdir(directory)
                except FileExistsError:
                    print("Already exists")
                
            with open(file, "w+") as file1:
                object = {
                    "main": {
                    "location":self.destination,
                    "server": self.Server,
                    "database": self.Database,
                    "username": self.Username,
                    "password": self.Password,
                    "encrypt": False,
                    "trustservercertificate": False,
                    "connectionTimeout": 30,
                    "port": 1433,
                    "table": self.Table,
                    "tags": [
                        "health",
                        "tv",
                        "games",
                        "anime",
                        "food",
                        "anime2"
                    ]
                    }
                }
                
                json.dump(object, file1, indent=3)
            
            if(not(pathlib.Path(self.destination).is_dir())):
                os.mkdir(self.destination)
                #subprocess.run(["pyinstaller", "updatQueAnsInstallerDemo.py", "--onefile", "--distpath", str(self.destination), "--add-binary"])
            shutil.copy(application_path + "/HNBAdminDemo.exe", self.destination)
            
            if(shortcutVar.get() == 1):
                aString = f"""$WshShell = New-Object -comObject WScript.Shell
                $Shortcut = $WshShell.CreateShortcut("{os.path.expanduser("~")}\Desktop\HNBAdmin.lnk")
                $Shortcut.TargetPath = "{application_path + "/HNBAdminDemo.exe"}"
                $Shortcut.Save()"""
                print(aString)
                subprocess.run(["powershell", aString])
            
            self.master.destroy()
        
        Back = tk.Button(Bottom, text="Back", width=self.btnWidth, font=self.btnFont, command=lambda:self.testConnection())
        #Back.config(state="disabled", background="lightgray")
        install = tk.Button(Bottom, text="Install", width=self.btnWidth, font=self.btnFont, command=lambda:Install())
        Back.grid(row=0, column=0, sticky="e", pady=5, padx=4)
        install.grid(row=0, column=1, sticky="e", pady=5, padx=4)
        
        Top.pack(side="top")
        Center.pack(after=Top, anchor="center", expand=True)
        Bottom.pack(side="bottom")
root = tk.Tk()
App(root)
root.mainloop() 