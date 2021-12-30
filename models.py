from project import app,mysql
from datetime import datetime
from flask_login import UserMixin

class User():
	cur1=mysql.connection.cursor()
	name=cur1.execute("Select name from flaskuser")
	email=cur1.execute("Select email from flaskuser")
	password=cur1.execute("Select pass from flaskuser")
	confirm_password=cur1.execute("Select cp from flaskuser")
	if name>0:
		all_name=cur1.fetchall()
	if confirm_password>0:
		all_confirm_password=cur1.fetchall()
	if email>0:
		all_email=cur1.fetchall()
	if password>0:
		all_password=cur1.fetchall()