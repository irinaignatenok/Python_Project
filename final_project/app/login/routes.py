import flask
import flask_login
import jwt

from . import blueprint
from . import forms, models
from . import send_mail
import random
# from .. main import models

# @blueprint.route("/")
# def home():
#     products = models.User.query.all()
#     return flask.render_template("home.html", products = products)


@blueprint.route("/sign-up/", methods = ["GET", "POST"])
def add_user():
    form = forms.SignupForm()
    if flask.request.method == "POST":
        if form.validate_on_submit():
            user = models.User(
                name = form.username.data.lower(),
                email = form.email.data,
            )
            user.set_password(form.password.data)

            if user.save():
                flask.flash(f"User {user.name} created successfully", category="success")
            else:
                flask.flash("Something went wrong...", category = "danger")
            return flask.redirect("/")
    return flask.render_template("signup.html", form = form)

@blueprint.route("/sign-in/", methods = ["GET", "POST"])
def signin():
    form = forms.SigninForm()
    if flask.request.method == "POST":
        if form.validate_on_submit():
          user = models.User.query.filter_by(name = form.username.data).first()
          if user is None:
              flask.flash("User does not exist...")
              return flask.redirect("/sign-in/")
          elif (form.username.data == 'andrei') and (form.password.data == '456'):
             flask.flash(f"Welcome admin, {user.name.title()}", category = "success")
             return flask.redirect('/admin')
          else:
              if user.check_password(form.password.data):
                  flask_login.login_user(user)
                  flask.flash(f"Welcome, {user.name.title()}", category = "success")
                  return flask.redirect('/')
              else:
                  flask.flash("Wrong credentials", category = "danger")
    return flask.render_template("signin.html", form = form)
@blueprint.route('/admin')
def admin_page():
    return flask.render_template("admin.html")

@blueprint.route("/reset_password/", methods = ["GET", "POST"])
def reset_password():
    form = forms.ResetPasswordForm()
    if flask.request.method == "POST":
        if form.validate_on_submit():
            user = models.User.query.filter_by(email = form.email.data).first()
            if user is not None:
                pwd_len = random.randint(8,12)
                pwd = ""

                for i in range(pwd_len):
                    pwd +=random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+''")

                ## Create a JSON message that contains his new password
                payload = {
                    "user_id":user.id,
                    "new_pwd":pwd,
                }
                encoded = jwt.encode(
                    payload,
                    flask.current_app.config["SECRET_KEY"],
                    algorithm = "HS256",
                    )

                link = flask.url_for("login_blueprint.reset_password_after", payload=encoded, _external=True)
                send_mail(
                    subject="Password reset",
                    body=f"Hey {user.name} ! Follow this link to reset your password: {link}",
                    recipients=[user.email]
                    )
                flask.flash("Email has been sent to your email", category = "success")
                return flask.redirect("/")
            else:
                flask.flash("The mail address doesn't exist", category = "danger")
    return flask.render_template("reset_password.html", form = form)

@blueprint.route("/reset-password/<payload>")
def reset_password_after(payload):
    # Instead of generating a random password, send a form to the user so that he can reset
    # his own password

    decoded = jwt.decode(
        payload,
        flask.current_app.config["SECRET_KEY"],
        algorithms = ["HS512", "HS256"]
    )
    user_id = decoded["user_id"]
    new_pwd = decoded["new_pwd"]

    user = models.User.query.get(user_id)
    user.set_password(new_pwd)

    flask.flash("Password reset successfully", category = "success")

    return flask.redirect('/')

@blueprint.route('/sign-out/')
def signout():
    flask_login.logout_user()
    return flask.redirect('/')
