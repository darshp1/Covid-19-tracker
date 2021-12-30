from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from project.models import User

def check_email():
    # get email from you form data
    email = request.form.get("email")

    cur = mysql.connection.cursor()
    cs1 = cur.cursor()
    params = [email]
    # cursor return affected rows
    count = cs1.execute('select * from users where email=%s', params)  # prevent SqlInject

    if count == 0:
    	x=1
        # count 0 email
    else:
        # the email exists
        # and if you want to fetch the user's info
        user_info = cs1.fetchall()  # the user_info should be a tuple


    # close the connection
    cs1.close()
    conn.close() 

def check_name():
    # get email from you form data
    name = request.form.get("name")

    cur = mysql.connection.cursor()
    cs1 = cur.cursor()
    params = [name]
    # cursor return affected rows
    count = cs1.execute('select * from users where name=%s', params)  # prevent SqlInject

    if count == 0:
    	oops=2
        # count 0 email
    else:
        # the email exists
        # and if you want to fetch the user's info
        user_info = cs1.fetchall()  # the user_info should be a tuple


    # close the connection
    cs1.close()
    conn.close() 


class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),
        Length(min=3,max=20)])
    email=StringField('Email',validators=[DataRequired(),
        Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm_password',
                        validators=[DataRequired(),EqualTo('password')])
    phone=StringField('Phone',validators=[DataRequired(),
        Length(min=10,max=10)])
    submit=SubmitField('Sign up')

    def validate_username(self,username):
        user1=User.query.filter_by(username=username.data).first()
        if user1:
            raise ValidationError('This username is taken please choose another one')   

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This Email is registered, You can login directly')       

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),
        Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember me')
    submit=SubmitField('Login')
    

class UpdateAccountForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),
        Length(min=3,max=20)])
    email=StringField('Email',validators=[DataRequired(),
        Email()])
    picture=FileField('Update your Profile Picture from here',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')

    def validate_username(self,username):
        if username.data!=current_user.username:
            user1=User.query.filter_by(username=username.data).first()
            if user1:
                raise ValidationError('This username is taken please choose another one')   

    def validate_email(self,email):
        if email.data!=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This Email is registered, You can login directly')   

