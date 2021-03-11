import flask
import time
import os
import flask_login, flask_mail

from . import blueprint, db
from . import models, forms
from . import User
from . import mail_manager
from .. main.models import Product, Appointment, Reviews, Contact
from .. login import models
import datetime

@blueprint.route("/")
def home():

    return flask.render_template("home.html")

#ADDING NEW IMAGES

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
            products = Product.query.all()
            for pro in products:
                if product == pro:
                    flask.flash("The image is already added")
                    flask.redirect("")
                else:
                    user.sell_products.append(product)

                    product.save()

                    print(f"Saved product with pic at path: {product.pic_path}")
                    flask.flash("The product has been added", category = "success")
                    return flask.render_template("admin.html")
    return flask.render_template("new_product.html", form=form)
#all images

@blueprint.route('/all-images')
def all_images():
    images = Product.query.all()
    return flask.render_template("images_admin.html", images = images)
#DELETE images
@blueprint.route('/delete-images/<int:id>')
def delete_images(id):
    delete_images= Product.query.get_or_404(id)
    try:
        db.session.delete(delete_images)
        db.session.commit()
        flask.flash("The product was deleted successfully", category = "success")
        return flask.redirect("/admin")
    except:
        return "There was a problem canceleling the appointment..."

#FAVORITE PAGE

@blueprint.route("/user-favorite-product",defaults = {"prod_id":None}, methods = ["GET", "POST"])
@blueprint.route("/user-favorite-product/<int:prod_id>", methods = ["GET", "POST"])
def user_favorite_product(prod_id):
    require_user = flask_login.fresh_login_required
    if not flask_login.current_user.is_authenticated:
        return flask.render_template("login_signup.html")
    else:
        user = flask_login.current_user
        user_products = user.liked_products
        if flask.request.method == "POST":
            product = Product.query.filter_by(id = prod_id).first()
            user_products.remove(product)
            db.session.commit()

    return flask.render_template("user_page.html", user = user, products = user_products)


# CATEGORIES(COLORING, WEDDING HAIRSTYLES, EVENING HAIRSTYLES, HAIRCUTS)
@blueprint.route("/wedding-hairstyle",defaults = {"prod_id":None}, methods = ["GET", "POST"])
@blueprint.route("/wedding-hairstyle/<int:prod_id>", methods = ["GET", "POST"])
def wedding_hairstyles(prod_id):
    products = Product.query.filter_by(name = "wedding hairstyles").all()
    user = flask_login.current_user
    # print(user.liked_products)
    if flask.request.method == "POST":
        # user_like_id = flask.request.form.get("product_id")
        user_like_product = Product.query.filter_by(id = prod_id).first()
        user = flask_login.current_user
        user.liked_products.append(user_like_product)
        user_like_product.save()

    return flask.render_template("wedding_hairstyles.html", products = products)


#COLORING
@blueprint.route("/coloring",defaults = {"prod_id":None}, methods = ["GET", "POST"])
@blueprint.route("/coloring/<int:prod_id>", methods = ["GET", "POST"])
def coloring(prod_id):
    products = Product.query.filter_by(name = "coloring").all()
    user = flask_login.current_user
    if flask.request.method == "POST":
        # user_like_id = flask.request.form.get("product_id")
        user_like_product = Product.query.filter_by(id = prod_id).first()

        user = flask_login.current_user
        user.liked_products.append(user_like_product)
        user_like_product.save()
        print(user.liked_products)

        # return flask.render_template("user_page.html", products = user_like_product, user = user )

    return flask.render_template("coloring.html", products = products)
#EVENING HAIRSTYLES
@blueprint.route("/evening-hairstyle",defaults = {"prod_id":None}, methods = ["GET", "POST"])
@blueprint.route("/evening-hairstyle/<int:prod_id>", methods = ["GET", "POST"])
def evening_hairstyle(prod_id):
    products = Product.query.filter_by(name = "evening hairstyles").all()
    first_image = Product.query.filter_by(name = "evening hairstyles").first()
    user = flask_login.current_user
    if flask.request.method == "POST":
        # user_like_id = flask.request.form.get("product_id")
        user_like_product = Product.query.filter_by(id = prod_id).first()
        user = flask_login.current_user
        user.liked_products.append(user_like_product)
        user_like_product.save()
        print(user.liked_products)

        # return flask.render_template("user_page.html", products = user_like_product, user = user )

    return flask.render_template("evening_hairstyle.html", products = products)

#HAIRCUTS
@blueprint.route("/haircut",defaults = {"prod_id":None}, methods = ["GET", "POST"])
@blueprint.route("/haircut/<int:prod_id>", methods = ["GET", "POST"])
def haircut(prod_id):
    products = Product.query.filter_by(name = "haircut").all()
    user = flask_login.current_user
    if flask.request.method == "POST":
        # user_like_id = flask.request.form.get("product_id")
        user_like_product = Product.query.filter_by(id = prod_id).first()

        user = flask_login.current_user
        user.liked_products.append(user_like_product)
        user_like_product.save()
        print(user.liked_products)

        # return flask.render_template("user_page.html", products = user_like_product, user = user )

    return flask.render_template("haircut.html", products = products)

# Hair Straightening
@blueprint.route("/hair-straightening",defaults = {"prod_id":None}, methods = ["GET", "POST"])
@blueprint.route("/hair-straightening/<int:prod_id>", methods = ["GET", "POST"])
def hair_straightening(prod_id):
    products = Product.query.filter_by(name = "hair straightening").all()
    user = flask_login.current_user
    if flask.request.method == "POST":
        # user_like_id = flask.request.form.get("product_id")
        user_like_product = Product.query.filter_by(id = prod_id).first()

        user = flask_login.current_user
        user.liked_products.append(user_like_product)
        user_like_product.save()
        print(user.liked_products)

    return flask.render_template("hair_straightening.html", products = products)


#APPOINTMENTS

@blueprint.route('/make-appointment', methods = ['POST','GET'])
def make_appointment():
    require_user = flask_login.fresh_login_required
    if not flask_login.current_user.is_authenticated:
        return flask.render_template("login_signup.html")
    else:
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
                flask.flash("Appointment booked successfully...", category = "success")
                return flask.redirect("/my-appointment")

    return flask.render_template("appointment.html", form = form)


@blueprint.route('/all-appointments')
def all_appointment():
    appointments = Appointment.query.all()
    return flask.render_template("all_appointments.html", appointments = appointments)

#MY APPOINTMENTS

@blueprint.route('/my-appointment', methods = ['POST', 'GET'])
def my_appointment():
    require_user = flask_login.fresh_login_required
    if not flask_login.current_user.is_authenticated:
        return flask.render_template("login_signup.html")
    else:
        user = flask_login.current_user
        user_appointments = user.user_appointment
        return flask.render_template("my_appointment.html", appointments = user_appointments, user = user)
# Delete appointment
@blueprint.route('/delete-appointment/<int:id>')
def delete_appointment(id):
    delete_appointment = Appointment.query.get_or_404(id)
    try:
        db.session.delete(delete_appointment)
        db.session.commit()
        flask.flash("The appointment was canceled successfully", category = "success")
        return flask.redirect("/my-appointment")
    except:
        return "There was a problem canceleling the appointment..."



@blueprint.route('/admin/trendy-hairstyle')
def admin_trendy():
    products = Product.query.filter_by(name = "evening hairstyle").all()
    return flask.render_template("trendy_hairstyles_admin.html", products = products)

#REVIEWS

@blueprint.route('/all-reviews')
def all_reviews():
    all_reviews = Reviews.query.all()
    return flask.render_template("all_reviews.html", reviews = all_reviews)

# ADMIN - Reviews
@blueprint.route('/admin-reviews')
def admin_reviews():
    reviews = Reviews.query.all()
    return flask.render_template("admin_reviews.html", reviews = reviews)

@blueprint.route('/delete-reviews/<int:id>')
def delete_review(id):
    reviews_to_delete = Reviews.query.get_or_404(id)

    try:
        db.session.delete(reviews_to_delete)
        db.session.commit()
        flask.flash("Review has been deleted...", category = "success")
        return flask.redirect('/admin-reviews')
    except:
        return "There was a problem deleting that post..."

# ADMIN APPOINTMENTS

@blueprint.route('/admin-delete-appointment/<int:id>')
def admin_delete_appointment(id):
    appointment_to_delete = Appointment.query.get_or_404(id)

    try:
        db.session.delete(appointment_to_delete)
        db.session.commit()
        flask.flash("Appointment has been deleted...", category = "success")
        return flask.redirect('/all-appointments')
    except:
        return "There was a problem deleting that appointment..."

#ADD_Reviews

@blueprint.route('/reviews', methods = ["GET", "POST"])
def reviews():
    require_user = flask_login.fresh_login_required
    if not flask_login.current_user.is_authenticated:
        return flask.render_template("login_signup.html")
    else:
        form = forms.ReviewsForm()
        if flask.request.method == "POST":
            if form.validate_on_submit():
                review = Reviews(
                    name = form.name.data,
                    reviews = form.reviews.data
                  )
                review.save()
                return flask.redirect("/all-reviews")
    return flask.render_template("reviews.html", form = form)
 #CONTACT

@blueprint.route('/contact', methods = ["GET", "POST"])
def contact():
    form = forms.ContactForm()
    if flask.request.method == "POST":
      if form.validate_on_submit():
          contact = Contact(
                name = form.name.data,
                phone = form.phone.data,
                email = form.email.data,
                message = form.message.data
          )
          contact.save()
          flask.flash("Your message has been sent...", category = "success")
          return flask.redirect('/')
    return flask.render_template('contact.html', form = form)

#MESSAGES
@blueprint.route('/messages')
def message():
    messages = Contact.query.all()

    return flask.render_template('messages.html', messages = messages)

#SEARCH
@blueprint.route("/search",defaults = {"prod_id":None}, methods = ["GET", "POST"])
@blueprint.route('/search/<int:prod_id>', methods = ['POST', 'GET'])
def search_product(prod_id):
    if flask.request.method == "POST":
        search = flask.request.form.get("pr_user")
        user_search = search.lower()
        products = Product.query.all()
        final_products = []
        # user_like_product = Product.query.filter_by(id = prod_id).first()

        for product in products:
            product_name = product.name
            product_description = product.description
            if (user_search in product_name) or (user_search in product_description):
                final_products.append(product)

        # user_like_product = Product.query.filter_by(id = prod_id).first()
        # user = flask_login.current_user
        # user.liked_products.append(user_like_product)
        # user_like_product.save()


        return flask.render_template("search.html",products = final_products )
