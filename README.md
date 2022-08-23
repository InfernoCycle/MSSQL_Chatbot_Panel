# MSSQL_Chatbot_Panel

# Description
App That allows users that own a chatbot to alter the contents of it, such as the answers and questions of it.

# Getting Started
To get started download the HNBAdminDemo.exe file and open it. To connect to your server that contains the chatbot contents, go to the settings page on the opened app and enter in the information in the named fields.

#Build Status
Some problems that will occur is notification modals will not spawn within the main window, and some lag may occur. Also if you have anti-virus software it may prevent you from using the app. To fix this just allow the app to be trusted by your anti-virus.

# How To Use?
The first page is the Home page, this is where you can add an answer to any question that doesn't have one. simply choose a question from the dropdown menu and enter the answer in the textfield below.

![image](https://user-images.githubusercontent.com/105338348/186277694-897e126b-7aee-40d7-bdb8-aba0cc356cbb.png)

Add page is where you can add a question, answer pair and a tag. Enter a question in the first textbox then a answer in the second textbox. You can then choose a tag (not required) or add a tag that may not be there.

Change page is where you can modify the question and answer. Just choose a question from the drop down menu and the two text boxes below will be filled with the question and answers respectively. You will be able to type or delete anything in them and submit when finished.

Settings page is where you set the database credentials to connect to your server that the chatbot is using. The first 5 field entrys are required to connect to the database (with an exception of Table field but without it you won't get any questions loaded in the app)

# Azure SQL Help setup
https://docs.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql&tabs=azure-portal

# Table Format
Make sure your table has the columns below (no capitalization): 
(id, question, answer, tag)
