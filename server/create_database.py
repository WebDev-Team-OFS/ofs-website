import mysql.connector



#update password to whatever you set your msql password to
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",    
    auth_plugin = 'mysql_native_password'
)

cursor = mydb.cursor();

cursor.execute("CREATE DATABASE IF NOT EXISTS accounts_db")

cursor.execute("USE accounts_db")
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    username VARCHAR(50),
    password VARCHAR(255)
)
""")

username = "john"
password = "pass123"
cursor.execute("INSERT INTO accounts (username, password) VALUES (%s, %s)", (username, password))
mydb.commit()

username = "bobby"
password = "loxd"
cursor.execute("INSERT INTO accounts (username, password) VALUES (%s, %s)", (username, password))
mydb.commit()

username = "bjork"
password = "vespertine"
cursor.execute("INSERT INTO accounts (username, password) VALUES (%s, %s)", (username, password))
mydb.commit()



cursor.execute("SELECT * FROM accounts")
for user in cursor.fetchall():
    print(user)

cursor.close();
mydb.close();