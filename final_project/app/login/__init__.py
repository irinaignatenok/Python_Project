import flask

from app.utils import ModelMixin
from app import db, login_manager
from app.utils import send_mail

blueprint = flask.Blueprint("login_blueprint", __name__, template_folder = "templates/")

from . import routes
