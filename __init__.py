from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY']='29484jfjeduwi949394'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dar$h19d'
app.config['MYSQL_DB'] = 'mysql'
bcrypt=Bcrypt(app)

mysql = MySQL(app)

from project import routes