import flask_login

from . import ModelMixin
from . import DeleteItem
from . import db


#Secondary table for User <-> Product relationship
products_likes = db.Table("products_likes",
                    db.Column("user_id", db.ForeignKey('user.id'), primary_key = True),
                    db.Column("product_id", db.ForeignKey("product.id"), primary_key = True)
                    )
#SECONDARY TABLE FOR USER <-> APPOINTMENT relationship
appointment_user = db.Table("appointment_user",
                        db.Column("user_id", db.ForeignKey('user.id'), primary_key = True),
                        db.Column("product_id", db.ForeignKey("appointment.id"), primary_key = True)
                        )

class Product(db.Model, ModelMixin, DeleteItem):
    __searchable__ = ['name', 'description']
    id = db.Column(db.Integer(), primary_key = True)
    # title       = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100), nullable = False)
    pic_path = db.Column(db.String(512))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def pic_html(self):
        return f'<img src = "{self.get_pic_url()} height = 150 width = 150">'

    def get_pic_url(self):
        return "/static/uploads/" + self.pic_path

class Reviews(db.Model,ModelMixin):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(64))
    reviews = db.Column(db.String(200))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

class Contact(db.Model, ModelMixin):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(64))
    phone = db.Column(db.Integer())
    email = db.Column(db.String(64), unique = True, nullable = False)
    message = db.Column(db.Text)

class Appointment(db.Model, ModelMixin):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(64))
    phone = db.Column(db.Integer(), nullable = False)
    date = db.Column(db.DateTime())
    description = db.Column(db.String(64))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    # def save(self):
    #     db.session.add(self)
    #     try:
    #         db.session.commit()
    #         return True
    #     except:
    #         db.session.rollback()
    #         return False
