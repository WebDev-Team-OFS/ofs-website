from flask import Flask

from flask_sqlalchemy import SQLAlchemy
#from flask_mysqldb import MySQL

app = Flask(__name__)


#update url with password
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/accounts'
@app.route('/')
def index():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True)