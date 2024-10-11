# Set Up Guide
## 0. Prerequisites
<a href="https://www.python.org/downloads/" target="_blank">Python 3.12.x</a><br/>
<a href="https://nodejs.org/en/download/package-manager" target="_blank">Node.js</a>

## 1. Install MySQL
Install here: https://dev.mysql.com/downloads/installer/ <br/>
Make sure to select your corresponding operating system.
Install MySQL Workbench too if it doesn't come with the default installation.

## 2. Clone the Repository Your System
 1. Open Command Prompt/Powershell on Windows or Terminal on Mac
 2. Change into the directory that you want to put the project in
    e.g:
    > cd Desktop
 3. Clone the repo and go into it
    > git clone https://github.com/CMPE131-Team-3/ofs-website.git<br/>
    > cd react-flask-template <br/>
    > code . <br/>
    
    *This should open the project in VSCode
## 3. Set Up Each Folder
 4. Open a new Terminal inside VSCode
    > For Windows: Ctrl + Shift + `
    > 
    > For Mac: Command + Shift + `
 5. Open client folder
    >cd client <br/>
    >npm install<br/>
    >npm run dev<br/>
 6. Open a different terminal to set up server
    >cd server <br/>
    >Windows: py -3 -m venv .venv  <br/>
    >Windows: .venv\Scripts\activate  <br/>
    
    >Mac: python3 -m venv .venv  <br/>
    >Mac: source .venv/bin/activate  <br/>
    
    *Note that for Windows, you might run into an error where you don't have permissions to activate the Virtual Environment. If so, then you will have to open a Command Prompt and activate it there instead of using VSCode terminal.
 7. Install from requirements.txt
    >Make sure your virtual environment is active<br/>
    >pip install -r requirements.txt
 8. Run the backend server
    >python main.py <br/>
    OR<br/>
    >python3 main.py<br/>
    
    *Open the server and in the URL add /api/users to the end of the URL
 9. Go to the frontend server and refresh it. If it is working properly, you will see a list of names.
## 4. Test MySQL database
 1. Open the create_database.py file and update the password in the connector to whatever your MySQL password is.
 2. Run the file.
 3. If it works correctly, it should print out some usernames and passwords. If you go on MySQL workbench and refresh the SCHEMAS, you should see the new database. 
 
