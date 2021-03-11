import flask_login
import werkzeug
from werkzeug import security
from . import db
from . import ModelMixin
from . import DeleteItem
class User(db.Model, flask_login.UserMixin, ModelMixin, DeleteItem):

    id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    name = db.Column(db.String(64), nullable = False, unique = True)
    email = db.Column(db.String(512))
    password = db.Column(db.String(512), nullable = False)

    sell_products = db.relationship("Product", backref = "seller")
    liked_products = db.relationship("Product", secondary = "products_likes",
                                        backref = 'likers')
    user_appointment = db.relationship("Appointment", secondary = "appointment_user", backref = "appointment_user")

    def set_password(self, new):
        pwd_hash = security.generate_password_hash(new)
        self.password = pwd_hash

    def check_password(self, pwd):
        return security.check_password_hash(self.password, pwd   )
