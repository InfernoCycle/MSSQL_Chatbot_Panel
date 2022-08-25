from cgitb import text
import os
import string
from tkinter import END, Button, StringVar, Tk, Toplevel, ttk
import tkinter as tk
from typing_extensions import IntVar
import pyodbc
import json
import pathlib


#path = os.path.dirname(__file__) + "/HNBAdmin/settings.json"
#file = ""

directory = os.path.expanduser("~") + "/AppData/Roaming/HNBAdmin/"
filePath = directory + "settings.json"

if(not (pathlib.Path(filePath).is_file())):
    #directory = os.path.join(os.path.dirname(__file__), "admin")
    #print(os.path.dirname(__file__) + "/admin")
    os.mkdir(directory)
    with open(filePath, "w+") as file1:
      object = {
          "main": {
              "location":"",
              "server": "",
              "database": "",
              "username": "",
              "password": "",
              "encrypt": False,
              "trustservercertificate": False,
              "connectionTimeout": 30,
              "port": 1433,
              "table": "",
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
      
else:
  pass
  #file = open(file, "r+")

class Applet(Tk):
  def __init__(self, master):
    self.server = None
    self.database = None
    self.username = None
    self.password = None
    self.cnxn = None
    self.cursor = None
    self.JsonFile = None
    self.table = None
    self.tags = None
    self.isConnected = "Not Connected"
    self.EncryptOption = "no"
    self.TrustOption = "no"
    
    self.btnFont = ("times new roman", 12, "bold")
    try:
      self.JsonFile = json.load(open(filePath))
    except json.JSONDecodeError:
      self.HomePage()
    
    if(self.JsonFile != None):
      self.server = self.JsonFile["main"]["server"]
      self.database = self.JsonFile["main"]["database"] 
      self.username = self.JsonFile["main"]["username"] 
      self.password = self.JsonFile["main"]["password"]
      self.table = self.JsonFile["main"]["table"]
      self.tags = self.JsonFile["main"]["tags"]
      self.encrypt = self.JsonFile["main"]["encrypt"]
      self.trustCert = self.JsonFile["main"]["trustservercertificate"]
      
      if(self.server == "" or self.database == "" or self.username == "" or self.password == ""):
        pass
          #print("was empty one of these")
      else:
        try:
          if(self.trustCert == False):
            self.TrustOption = "no"
          else:
            self.TrustOption = "yes"
          
          if(self.encrypt == False):
            self.EncryptOption = "no"
          else:
            self.EncryptOption = "yes"
            
          self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password + ";Encrypt=" + self.EncryptOption + ";Trusted_Connection=" + self.TrustOption)
          self.cursor = self.cnxn.cursor()
          self.cursor.execute(f"select id, question from {self.table} where answer is null")
          self.isConnected = "Connected"
        except:
          pass
          #print("No query was able to run Line 81")
        
      self.Questions = list()

      try:
        for question in self.cursor.fetchall():
          self.Questions.append(question[0] + ", " + question[1])

        self.sort(self.Questions)
      except:
        pass
        #print("No query was able to run Line 91")

      self.master = master
      self.master.title("Bot Admin Panel")
      self.master.eval("tk::PlaceWindow . center")
      self.master.geometry("500x450")
      self.master.maxsize(600, 540)
      self.master.minsize(400, 370)
      self.master.grid_columnconfigure([0,1], weight=1)
      self.master.grid_rowconfigure([0,1,2,3,4,5], weight=1)

      style = ttk.Style(self.master)
      style.theme_use("winnative")

      self.HomePage()
    
    else:
      pass
  
  def close(self):
    self.cursor.close()

  def HomePage(self):
    for i in self.master.winfo_children():
        #print(i)
        i.destroy()
    
    def add():
      self.cursor.execute(f"update {self.table} set answer = ? where question = ?", EntryAnswer.get("1.0", END), strVar.get())
      self.cursor.commit()
      Top = Toplevel(Panel)
      Top.title("Submit")
      Top.geometry("200x100")
      Top.config(bg="gray")
      Top.grid_columnconfigure([0], weight=1)
      Top.grid_rowconfigure([0], weight=1)
      
      Notify = tk.Label(Top, text="Changes Saved")
      Notify.grid(row=0, column=0)

    Panel = tk.Frame(self.master)

    Panel.grid_rowconfigure([0,1,2,3,4,5,6], weight=1)
    Panel.grid_columnconfigure([0, 1], weight=1)

    ButtonPanel = tk.Frame(Panel)
    
    ButtonPanel.grid_columnconfigure([0,1,2,3], weight=1)

    strVar = tk.StringVar(Panel)
    
    self.cursor.execute(f"select question from {self.table} where answer is null")
    temp = self.cursor.fetchall()
    #question = list()
    question = [item[0] for item in temp]
    #for item in temp:
     # question.append(item[0])
    
    addBtn = tk.Button(ButtonPanel, text="Add", command=lambda:self.Add(), width=10, fg="red", font=self.btnFont)
    ChangeBtn = tk.Button(ButtonPanel, text="Change", command=lambda:self.ChangePage(), width=10, fg="red", font=self.btnFont)
    homeBtn = tk.Button(ButtonPanel, text="Home", state="normal", fg="red", width=10, font=self.btnFont, bg="lightgreen")
    settingsBtn = tk.Button(ButtonPanel, text="Settings", command=lambda:self.settings(), fg="red", width=10, font=self.btnFont)

    QuestionLabel = ttk.Label(Panel, text="Choose question (Questions here do not have an answer):")
    self.Combobox = ttk.Combobox(Panel, textvariable=strVar, values=question, width=40)

    AnswerLabel = ttk.Label(Panel, text="Enter an answer for chosen quetion: ")
    EntryAnswer = tk.Text(Panel, height=3)

    submit = tk.Button(Panel, text="Submit", width=10, command=lambda:add(), font=self.btnFont, fg="red")

    addBtn.grid(row=0, column=1, sticky="n", padx=10, pady=5)
    ChangeBtn.grid(row=0, column=2, sticky="n", padx=10, pady=5)
    homeBtn.grid(row=0, column=0, sticky="n", padx=10, pady=5)
    settingsBtn.grid(row=0, column=3, sticky="n", padx=10, pady=5)

    QuestionLabel.grid(row=1, column=0, columnspan=2)
    self.Combobox.grid(row=2, column=0, padx=10)
    AnswerLabel.grid(row=3, column=0)
    EntryAnswer.grid(row=4, column=0, pady=5, padx=10)
    submit.grid(row=5, column=0, pady=5)

    ButtonPanel.grid(row=0,column=0)
    Panel.grid(column=0, row=0)

  def sort(self, arr:list()):
    if(len(arr) > 1):
      mid = len(arr) // 2

      left = arr[0:mid]
      right = arr[mid:len(arr)-1]

      self.sort(left)
      self.sort(right)

      l = 0
      k=0
      r=0

      while(l < len(left) and r < len(right)):
        if(left[l] < arr[k]):
          arr[k] = left[l]
          l+=1
        else:
          arr[k] = right[r]
          r+=1
        k+=1
      
      while(l < len(left)):
        arr[k] = left[l]
        l+=1
        k+=1
      
      while(r < len(right)):
        arr[k] = left[r]
        r+=1
        k+=1

  def findIndex(self, searchValue):
    lowerbound = 0
    upperbound = len(self.Questions)

    while(True):
      if(upperbound < lowerbound):
        break

      midpoint = int(lowerbound + (upperbound - lowerbound) / 2)

      if(self.Questions[midpoint] < searchValue):
        lowerbound = midpoint + 1
      
      if(self.Questions[midpoint] > searchValue):
        upperbound = midpoint - 1
      
      if(self.Questions[midpoint] == searchValue):
        return midpoint
      
  def Add(self):
    for i in self.master.winfo_children():
      i.destroy()
    labelVar = StringVar()
    
    def submission():
      if(QuestionEntry.get("1.0", END).strip() != "" and AnswerEntry.get("1.0", END).strip() != "" and QuestionEntry.get("1.0", END).strip() != None and AnswerEntry.get("1.0", END).strip() != None):
        self.cursor.execute("insert into " + self.table + "(question, answer, tag) values(?, ?, ?)", QuestionEntry.get("1.0", END).strip(), AnswerEntry.get("1.0", END).strip(), tagVar.get().strip())
        self.cursor.commit()
        Top = Toplevel(Panel)
        Top.title("Submit")
        Top.geometry("200x100")
        Top.config(bg="gray")
        Top.grid_columnconfigure([0], weight=1)
        Top.grid_rowconfigure([0], weight=1)
        
        Notify = tk.Label(Top, text="Changes Saved")
        Notify.grid(row=0, column=0)
      else:
        Pop = Toplevel(Panel) 
        Pop.geometry("100x100")
        Pop.grid_rowconfigure([0], weight=1)
        Pop.grid_columnconfigure([0], weight=1)
        alert = tk.Label(Pop, wraplength=100,text="Can't leave question or answer blank")
        alert.grid(row=0, column=0)
    
    def modal():
      def add():
        if(labelVar not in self.tags):
          self.tags.append(TagName.get())
          file = open(filePath, "r+")
          file.truncate()
          file.seek(0)
          self.JsonFile["main"]["tags"] = self.tags
          json.dump(self.JsonFile, file, indent=3)
          pop.destroy()
          Panel.update()
          Panel.update_idletasks()
      
      pop = Toplevel(Panel)
      
      pop.geometry("170x170")
      pop.maxsize(200,200)
      pop.minsize(140,140)
      pop.grid_rowconfigure([0,1,2], weight=1)
      pop.grid_columnconfigure([0], weight=1)
      
      TagLbe = tk.Label(pop, text="Enter Tag Name:")
      TagName = ttk.Entry(pop, textvariable=labelVar)
      save = tk.Button(pop, text="Save", font=self.btnFont, command=lambda:add())
      
      TagLbe.grid(row=0, column=0, padx=10)
      TagName.grid(row=1, column=0, padx=10)
      save.grid(row=2, column=0, padx=10)
        
    Panel = tk.Frame(self.master)
    Panel.grid_rowconfigure([0,1,2,3,4,5,6,7], weight=1)
    Panel.grid_columnconfigure([0], weight=1)
    ButtonPanel = ttk.Frame(Panel)
    ButtonPanel.grid_columnconfigure([0,1,2,3], weight=1)
    
    tagVar = StringVar()
    
    homeBtn = tk.Button(ButtonPanel, text="Home", command=lambda:self.HomePage(), width=10, fg="red", font=self.btnFont)
    changeBtn = tk.Button(ButtonPanel, text="Change", command=lambda:self.ChangePage(), width=10, fg="red", font=self.btnFont)
    addBtn = tk.Button(ButtonPanel, text="Add", width=10, fg="red", font=self.btnFont, bg="lightgreen")
    settingsBtn = tk.Button(ButtonPanel, text="Settings", command=lambda:self.settings(), fg="red", font=self.btnFont, width=10)

    QuestionLabel = ttk.Label(Panel, text="Enter Question: ")
    QuestionEntry = tk.Text(Panel, height=3)

    AnswerLabel = ttk.Label(Panel, text="Enter Answer: ")
    AnswerEntry = tk.Text(Panel, height=3)
    
    TagCombobox = ttk.Combobox(Panel, textvariable=tagVar, values=self.tags)
    TagBtn = tk.Button(Panel, text="Click to add tag", fg="blue", borderwidth=0, command=lambda:modal())

    Submit = tk.Button(Panel, text="Submit", width=10, fg="red", font=self.btnFont, command=lambda:submission())

    homeBtn.grid(row=0, column=0, padx=10, pady=5)
    changeBtn.grid(row=0, column=2, padx=10, pady=5)
    addBtn.grid(row=0, column=1, padx=10, pady=5)
    settingsBtn.grid(row=0, column=3, padx=10)

    QuestionLabel.grid(row=1, column=0)
    QuestionEntry.grid(row=2, column=0, padx=10)
    AnswerLabel.grid(row=3, column=0)
    AnswerEntry.grid(row=4, column=0, padx=10)
    TagCombobox.grid(row=5, column=0, padx=10, pady=10)
    TagBtn.grid(row=6, column=0)
    
    Submit.grid(row=7, column=0, pady=10)
    ButtonPanel.grid(row=0, column=0)
    Panel.grid(row=0, column=0)

  def ChangePage(self): #reinvent this and change up again to show the chosen id question and stuff
    for i in self.master.winfo_children():
        i.destroy()
    
    Question = list()
    try:
      self.cursor.execute(f"select question from {self.table}")
      for y in self.cursor.fetchall():
        Question.append(y[0])
    except:
      pass
      #print("Could not run sql query")

    def change(e):
      #print(stringVarQuestion.get().strip())
      self.cursor.execute(f"select id, question, answer from {self.table} where question = ?", stringVarQuestion.get().strip())
      data = self.cursor.fetchall()
      idVar.set(data[0][0])
      QuestionChgEntry.delete("1.0", END)
      QuestionChgEntry.insert("1.0", data[0][1])
      AnswerChgEntry.delete("1.0", END)
      AnswerChgEntry.insert("1.0", data[0][2])
      #QuestionChgEntry.insert("1.0", )
      
    def submission():
      if(QuestionChgEntry.get("1.0", END).strip() == ""):
        return

      self.cursor.execute(f"update {self.table} set question = ?, answer = ? where " +
                          f"id={idVar.get().strip()}", QuestionChgEntry.get("1.0", END).strip(), AnswerChgEntry.get("1.0", END).strip())
      self.cursor.commit()

      Top = Toplevel(Panel)
      Top.title("Submit")
      Top.geometry("200x100")
      Top.config(bg="gray")
      Top.grid_columnconfigure([0], weight=1)
      Top.grid_rowconfigure([0], weight=1)
      
      Notify = tk.Label(Top, text="Changes Saved")
      Notify.grid(row=0, column=0)
      
    Panel = ttk.Frame(self.master)
    Panel.grid_columnconfigure([0,1], weight=1)
    Panel.grid_rowconfigure([0,1,2,3,4,5,6], weight=1)
    
    idVar = StringVar(Panel)
    ButtonPanel = ttk.Frame(Panel)
    ButtonPanel.grid_columnconfigure([0,1,2,3], weight=1)
    
    homeBtn = tk.Button(ButtonPanel, text="Home", command=lambda:self.HomePage(), fg="red", font=self.btnFont, width=10)
    addBtn = tk.Button(ButtonPanel, text="Add", command=lambda:self.Add(), fg="red", font=self.btnFont, width=10)
    changeBtn = tk.Button(ButtonPanel, text="Change", fg="red", font=self.btnFont)
    changeBtn.config(state="normal", width=10, bg="lightgreen")
    settingsBtn = tk.Button(ButtonPanel, text="Settings", command=lambda:self.settings(), fg="red", font=self.btnFont, width=10)

    stringVar = StringVar(Panel, value="0")
    stringVarQuestion = StringVar(Panel)

    QuestionLabel = ttk.Label(Panel, text="Question")
    QuestionCombobox = ttk.Combobox(Panel, textvariable=stringVarQuestion, values=Question, width=47)
    QuestionCombobox.bind("<<ComboboxSelected>>", change)
    QuestionChgLabel = ttk.Label(Panel, text="Change Question Here: ")
    QuestionChgEntry = tk.Text(Panel, height=5)
    #QuestionChgEntry.configure(state="disabled")

    #####-------------------Answer section--------------------------------------

    AnswerChgLabel = ttk.Label(Panel, text="Change Answer Here: ")
    AnswerChgEntry = tk.Text(Panel, height=5)

    Submit = tk.Button(Panel, text="Submit", command=lambda:submission(), font=self.btnFont, fg="red")
    
    homeBtn.grid(row=0, column=0, padx=10, pady=5)
    addBtn.grid(row=0, column=1, padx=10, pady=5)
    changeBtn.grid(row=0, column=2, padx=10, pady=5)
    settingsBtn.grid(row=0, column=3, padx=10, pady=5)
    ButtonPanel.grid(row=0, column=0, pady=5)

    QuestionLabel.grid(row=1, column=0)
    QuestionCombobox.grid(row=2, column=0, padx=10)
    QuestionChgLabel.grid(row=3, column=0)
    QuestionChgEntry.grid(row=4, column=0, padx=10)

    AnswerChgLabel.grid(row=5, column=0)
    AnswerChgEntry.grid(row=6, column=0, padx=10)
    Submit.grid(row=7, column=0, pady=5)
    Panel.grid(row=0, column=0)
  
  def settings(self):
    for i in self.master.winfo_children():
      i.destroy()
    
    def encryptChange():
      pass
      #print(EncryptVar.get())
    
    def trustCertChange():
      pass
      #print(TrustServerCertVar.get())
    
    def save(self):
      #print(filePath)
      #print(ServerEntry.get("1.0", END))
      #print(DatabaseEntry.get("1.0", END).strip())
      #print(UsernameEntry.get("1.0", END).strip())
      #print(PasswordEntry.get("1.0", END).strip())
      file1 = open(filePath, "w+")
      file1.seek(0)
      file1.truncate()
      self.JsonFile["main"]["server"] = ServerEntry.get("1.0", END).strip()
      self.JsonFile["main"]["database"] = DatabaseEntry.get("1.0", END).strip()
      self.JsonFile["main"]["username"] = UsernameEntry.get("1.0", END).strip()
      self.JsonFile["main"]["password"] = PasswordEntry.get("1.0", END).strip()
      self.JsonFile["main"]["table"] = TableEntry.get("1.0", END).strip()
      
      self.Server = ServerEntry.get("1.0", END).strip()
      #ServerEntry.insert("1.0", self.Server)
      self.Database = DatabaseEntry.get("1.0", END).strip()
      #DatabaseEntry.insert("1.0", self.Database)
      self.Username = UsernameEntry.get("1.0", END).strip()
      #UsernameEntry.insert("1.0", self.Username)
      self.Password = PasswordEntry.get("1.0", END).strip()
      #PasswordEntry.insert("1.0", self.Password)
      self.Table = TableEntry.get("1.0", END).strip()
      #TableEntry.insert("1.0", self.Table)
      
      #print(self.JsonFile)
      if(EncryptVar.get() == 0):
        self.JsonFile["main"]["encrypt"] = False
      elif(EncryptVar.get() == 1):
        self.JsonFile["main"]["encrypt"] = True
      if(TrustServerCertVar.get() == 0):
        self.JsonFile["main"]["trustservercertificate"] = False
      elif(TrustServerCertVar.get() == 1):
        self.JsonFile["main"]["trustservercertificate"] = True
      json.dump(self.JsonFile, file1, indent=3)
      file1.close()
      
      self.__init__(self.master)
      
    Panel = ttk.Frame(self.master)
    Panel.grid_columnconfigure([0,1], weight=1)
    Panel.grid_rowconfigure([0,1,2,3,4,5,6,7,8,9,10,11,12], weight=1)

    ButtonPanel = ttk.Frame(Panel)
    ButtonPanel.grid_columnconfigure([0,1,2,3], weight=1)
    
    PermsPanel = ttk.Frame(Panel)
    PermsPanel.grid_rowconfigure([0], weight=1)
    PermsPanel.grid_columnconfigure([0,1], weight=1)
    
    homeBtn = tk.Button(ButtonPanel, text="Home", command=lambda:self.HomePage(), fg="red", font=self.btnFont, width=10)
    addBtn = tk.Button(ButtonPanel, text="Add", command=lambda:self.Add(), fg="red", font=self.btnFont, width=10)
    changeBtn = tk.Button(ButtonPanel, text="Change", command=lambda:self.ChangePage(), fg="red", font=self.btnFont, width=10)
    settingsBtn = tk.Button(ButtonPanel, text="Settings", fg="red", font=self.btnFont, width=10)
    settingsBtn.config(state="normal", bg="lightgreen")
    
    EncryptVar = tk.IntVar(PermsPanel, value=int(self.encrypt))
    TrustServerCertVar = tk.IntVar(PermsPanel, value=int(self.trustCert))
    
    ServerLabel = ttk.Label(Panel, text="Server:")
    ServerEntry = tk.Text(Panel, height=1)
    ServerEntry.insert("1.0", self.server)
    
    DatabaseLabel = ttk.Label(Panel, text="Database:")
    DatabaseEntry = tk.Text(Panel, height=1)
    DatabaseEntry.insert("1.0", self.database)
    
    TableLabel = tk.Label(Panel, text="Table:")
    TableEntry = tk.Text(Panel, height=1)
    TableEntry.insert("1.0", self.table)
    
    UsernameLabel = ttk.Label(Panel, text="Username:")
    UsernameEntry = tk.Text(Panel, height=1)
    UsernameEntry.insert("1.0", self.username)
    
    PasswordLabel = ttk.Label(Panel, text="Password:")
    PasswordEntry = tk.Text(Panel, height=1)
    PasswordEntry.insert("1.0", self.password)
    
    saveBtn = tk.Button(Panel, text="Save", command=lambda:save(self), fg="red", font=self.btnFont, width=10)
    
    homeBtn.grid(row=0, column=0, padx=10)
    addBtn.grid(row=0,column=1, padx=10)
    changeBtn.grid(row=0,column=2, padx=10)
    settingsBtn.grid(row=0,column=3, padx=10)
    ButtonPanel.grid(column=0, row=0, padx=10, pady=5)
    
    ServerLabel.grid(row=1, column=0)
    ServerEntry.grid(row=2, column=0, padx=10)
    
    DatabaseLabel.grid(row=3, column=0)
    DatabaseEntry.grid(row=4, column=0, padx=10)
    
    TableLabel.grid(row=5,column=0)
    TableEntry.grid(row=6, column=0, padx=10)
    
    UsernameLabel.grid(row=7, column=0)
    UsernameEntry.grid(row=8, column=0, padx=10)
    
    PasswordLabel.grid(row=9, column=0)
    PasswordEntry.grid(row=10, column=0, padx=10)
    
    ConnectionTimeoutLabel = tk.Label(Panel, text="Connection Timeout Time (Default: 30): ")
    ConnectionTimeout = tk.Text(Panel, height=1)
    
    EncryptCheck = ttk.Checkbutton(PermsPanel, text="Encrypt", variable=EncryptVar, command=lambda:encryptChange())
    TrustCertCheck = ttk.Checkbutton(PermsPanel, text="TrustServerCertificate", variable=TrustServerCertVar, command=lambda:trustCertChange())
    
    StatusPanel = tk.Frame(self.master)
    StatusPanel.grid_columnconfigure([0], weight=1)
    StatusPanel.grid_rowconfigure([0], weight=1)
    Status = tk.Label(StatusPanel, text=f"Status: {self.isConnected}")
    Status.grid(row=0, column=0)
    
    EncryptCheck.grid(row=0, column=0)
    TrustCertCheck.grid(row=0, column=1)
    
    PermsPanel.grid(row=11, column=0, pady=5)
    ConnectionTimeoutLabel.grid(row=12, column=0)
    ConnectionTimeout.grid(row=13, column=0, padx=10)
    saveBtn.grid(row=14, column=0, pady=5)

    Panel.grid(row=0, column=0)
    StatusPanel.grid(row=1, column=0)
    
root = Tk()
Applet(root)
root.mainloop()