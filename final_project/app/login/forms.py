import flask_wtf
import wtforms
from wtforms import validators as vld
import string

##validators

def validate_username(form, field):

    if len(field.data) < 5:
        raise vld.ValidationError("Username has to be at least 5 characters")

    # for symbol in string.punctuation:
    #     if symbol in field.data:
    #         raise vld.ValidationError("No symbols allowed in username")


    if len(field.data) >=12:
        raise vld.ValidationError("Maximum characters allowed is 12")

def validate_password(form, field):

    password = field.data
    if password == password.lower():
        raise vld.ValidationError("Password need to contain at least one uppercased letter")

    if password == password.upper():
        raise vld.ValidationError("Password need to contain at least one lowercased letter")

    if not 8 <= len(password) <= 12:
        raise vld.ValidationError("Password length need to be between 8 and 12")


#Classes

class SigninForm(flask_wtf.FlaskForm):

    username = wtforms.StringField("Username: ")
    password = wtforms.PasswordField("Password: ")

    submit = wtforms.SubmitField("Sign in")

class SignupForm(flask_wtf.FlaskForm):

    username = wtforms.StringField("Username: ")
    email = wtforms.StringField("Email: ")
    password = wtforms.PasswordField("Password: ")


    submit = wtforms.SubmitField("Sign up")

class ResetPasswordForm(flask_wtf.FlaskForm):

    email = wtforms.StringField("Email: ")
    submit = wtforms.SubmitField("Submit ")
