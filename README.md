# MSSQL_Chatbot_Panel

# Description
App That allows users that own a chatbot to alter the contents of it, such as the answers and questions of it.

# Getting Started
To get started download the HNBAdminDemo [zip](https://github.com/InfernoCycle/MSSQL_Chatbot_Panel/archive/refs/tags/v1.1.9.zip) file and extract contents. create a shortcut for the HNBAdminDemo.exe file and move it anywhere. You should be all set to run it.

# After opening up program
To connect to your server that contains the chatbot contents, go to the settings page on the opened app and enter in the information in the named fields.

# Build Status
Some problems that will occur is notification modals will not spawn within the main window, and some lag may occur. Also if you have anti-virus software it may prevent you from using the app. To fix this just allow the app to be trusted by your anti-virus.

# How To Use?
The first page is the Home page, this is where you can add an answer to any question that doesn't have one. simply choose a question from the dropdown menu and enter the answer in the textfield below.

![image](https://user-images.githubusercontent.com/105338348/186277694-897e126b-7aee-40d7-bdb8-aba0cc356cbb.png)

Add page is where you can add a question, answer pair and a tag. Enter a question in the first textbox then a answer in the second textbox. You can then choose a tag (not required) or add a tag that may not be there.

![image](https://user-images.githubusercontent.com/105338348/186277918-58d3d613-842a-4c5a-aeaa-8442f747f40c.png)

Change page is where you can modify the question and answer. Just choose a question from the drop down menu and the two text boxes below will be filled with the question and answers respectively. You will be able to type or delete anything in them and submit when finished.

![image](https://user-images.githubusercontent.com/105338348/186277972-2e46063b-9a24-433a-b9ce-ea98ca5fb52d.png)

Settings page is where you set the database credentials to connect to your server that the chatbot is using. The first 5 field entrys are required to connect to the database (with an exception of Table field but without it you won't get any questions loaded in the app)

![image](https://user-images.githubusercontent.com/105338348/186278025-26047fe3-f6c0-4cf3-81fd-92e1468af4b3.png)

# Source Code
The Source Code is provided. Simply download the HNBAdminDemo.py file

# Azure SQL Help setup
https://docs.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql&tabs=azure-portal

# Table Format
Make sure your table has the columns below (no capitalization): 
(id, question, answer, tag)

# Supported Operating Systems
Windows 8.1 and Windows 10 are supported. (Other Window versions have not been tested as of yet)

# Not Supported Operating Systems
macOS and Linux are currently not supported.
