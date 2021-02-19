import os


basedir = os.path.abspath("app") #__file__is "__init__.py"

class Config:

    SECRET_KEY = "93d8bf9cd892026e9f3f8fef197ab918"
    UPLOAD_DIR = os.path.join(basedir, "static/uploads")
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:V8VcgPjA@localhost:5432/pyFinalProject"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WHOOSH_BASE = os.path.join(basedir, "whoosh")


    # Mail Config
