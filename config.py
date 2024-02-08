from os import path, environ
from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))


baseDB = path.join(BASE_DIR, 'app.db')

class BaseConfig(object):
    ENVIRONMENT = environ.get("ENVIRONMENT")
    SECRET_KEY = environ.get("SECRET_KEY")
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
  


class ProductionConfig(BaseConfig):
    ENVIRONMENT = environ.get("ENVIRONMENT")
    # Flask Config
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    SECRET_KEY = environ.get("SECRET_KEY")
    # Database
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + baseDB
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True


class StagingConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True