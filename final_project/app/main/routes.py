import flask
import time
import os
import flask_login, flask_mail

from . import blueprint, db
from . import models, forms
from . import User
from . import mail_manager
from .. main.models import Product, Appointment
from .. login import models
import datetime

@blueprint.route("/")
def home():

    return flask.render_template("home.html")



@blueprint.route("/product-new/", methods = ['GET', 'POST'])
def add_product():
    form = forms.NewProductForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            pic = form.pic.data

            pic_name = f"{int(time.time())}.jpg"
            pic_filename = os.path.join(flask.current_app.config["UPLOAD_DIR"], pic_name)
            pic.save(pic_filename)

            product = Product(
                name = form.name.data,
                description = form.description.data,
                pic_path = pic_name,
            )

            user = User.query.get(1)
            user.sell_products.append(product)
            product.save()

            print(f"Saved product with pic at path: {product.pic_path}")
            flask.flash("The product has been added")
            return flask.redirect("/trendy-hairstyle")
    return flask.render_template("new_product.html", form=form)


@blueprint.route('/make-appointment', methods = ['GET', 'POST'])
def make_appointment():
    form = forms.AppointmentForm()
    if flask.request.method == "POST":
        if form.validate_on_submit():
            date = datetime.datetime.combine(form.date.data, form.time.data)
            appointment = Appointment(
                    name = form.name.data,
                    phone = form.phone.data,
                    date = date,
                    description = form.description.data
            )
            user = flask_login.current_user
            user.user_appointment.append(appointment)
            appointment.save()
            flask.flash("Appointment booked successfully...")
            return flask.redirect("/my-appointment")
    return flask.render_template("appointment.html", form = form)


@blueprint.route('/all-appointments')
def all_appointment():
    appointments = Appointment.query.all()
    return flask.render_template("all_appointments.html", appointments = appointments)



@blueprint.route('/my-appointment', methods = ['POST', 'GET'])
def my_appointment():
    user = flask_login.current_user
    user_appointments = user.user_appointment

    return flask.render_template("my_appointment.html", appointments = user_appointments, user = user)


@blueprint.route("/trendy-hairstyle", methods = ['POST', 'GET'])
def trendy_hairstyles():
    products = Product.query.all()
    user = flask_login.current_user
    print(user.liked_products)
    if flask.request.method == "POST":
        user_like_id = flask.request.form.get("product_id")
        user_like_product = Product.query.filter_by(id = user_like_id).first()
        print(user_like_product)
        print(user_like_id)
        # print(user_like)
        user = flask_login.current_user
        user.liked_products.append(user_like_product)
        user_like_product.save()
        print(user.liked_products)

        # return flask.render_template("user_page.html", products = user_like_product, user = user )

    return flask.render_template("trendy_hairStyle.html", products = products)

@blueprint.route("/user-favorite-product")
def user_favorite_product():
    user = flask_login.current_user
    products = user.liked_products
    return flask.render_template("user_page.html", user = user, products = products)



@blueprint.route('/search', methods = ['POST'])
def search_product():
    if flask.request.method == "POST":
        user_search = flask.request.form.get("pr_user")
        products = Product.query.all()
        final_products = []

        for product in products:
            product_name = product.name
            product_description = product.description
            if (user_search in product_name) or (user_search in product_description):
                final_products.append(product)


        return flask.render_template("search.html",products = final_products )
