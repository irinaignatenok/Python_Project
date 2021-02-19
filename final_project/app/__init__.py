import flask
from flask_sqlalchemy import SQLAlchemy



import flask_migrate
import flask_login
import flask_mail




import os
import config



basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
migrate = flask_migrate.Migrate()
login_manager = flask_login.LoginManager()
mail_manager = flask_mail.Mail()

@login_manager.user_loader
def load_user(user_id):
    return login.models.User.query.get(user_id)

def create_app():

    from .login import blueprint as login_bp
    from .main import blueprint as main_bp

    #create the app controller
    app = flask.Flask(__name__)

    app.register_blueprint(login_bp)
    app.register_blueprint(main_bp)


    #Load the config directly from a class
    app.config.from_object(config.Config)

    # Initialize the app after everything has been read by python
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail_manager.init_app(app)
    

    @app.shell_context_processor
    def shel_predefined_variables():
        from .main import models
        from .login.models import User
        # from app.login import models


    return app
