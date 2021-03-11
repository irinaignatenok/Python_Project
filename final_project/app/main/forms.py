import flask_wtf
import wtforms
from wtforms.fields.html5 import DateField, TimeField

class NewProductForm(flask_wtf.FlaskForm):

    name = wtforms.StringField("Title: ")
    description = wtforms.TextAreaField("Description: ")
    pic = wtforms.FileField("Picture: ")
    submit = wtforms.SubmitField("Add Product")

class AppointmentForm(flask_wtf.FlaskForm):
    name = wtforms.StringField("Name: ")
    phone = wtforms.IntegerField("Phone: ")
    date = DateField("Date: ")
    time = TimeField("Time: ")
    description = wtforms.StringField("What kind of service would you like? ")
    submit = wtforms.SubmitField("Book an Appointment")

class ReviewsForm(flask_wtf.FlaskForm):

    name = wtforms.StringField("Name: ")
    reviews = wtforms.StringField("Reviews: ")

    submit = wtforms.SubmitField("Leave feedback: ")

class ContactForm(flask_wtf.FlaskForm):
    name = wtforms.StringField("Name: ")
    phone = wtforms.IntegerField("Phone: ")
    email = wtforms.StringField("Email: ")
    message = wtforms.TextAreaField("Message: ")
    submit = wtforms.SubmitField("Send: ")
