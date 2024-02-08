from flask import Flask
from flask_migrate import Migrate
from app.db.database import db
from flask_restful import Api
from app.resources.UserResource import UserCreate, UserDetail, UserList, UserUpdate, UserDelete
from app.resources.AccountResource import AccountCreate, AccountDetail, AccountList, AccountUpdate, AccountDelete
from app.services.AccountService import AccountService
from app.services.UserService import UserService


migrate = Migrate()

def create_app(config=None):
    user_service = UserService()
    account_service = AccountService()

    app = Flask(__name__, instance_relative_config=True)    
    if config is None:
        app.config.from_object("config.BaseConfig")
    else:
        app.config.from_object(config)
    api = Api(app)
    
    # Add resources for users
    api.add_resource(UserCreate, "/users", resource_class_kwargs={"user_service": user_service})
    api.add_resource(UserDetail, "/users/<int:id>", resource_class_kwargs={"user_service": user_service})
    api.add_resource(UserList, "/users", resource_class_kwargs={"user_service": user_service})
    api.add_resource(UserUpdate, "/users/<int:id>", resource_class_kwargs={"user_service": user_service})
    api.add_resource(UserDelete, "/users/<int:id>", resource_class_kwargs={"user_service": user_service})
    
    # Add resources for accounts
    api.add_resource(AccountCreate, "/accounts", resource_class_kwargs={"account_service": account_service})
    api.add_resource(AccountDetail, "/accounts/<int:id>", resource_class_kwargs={"account_service": account_service})
    api.add_resource(AccountList, "/accounts", resource_class_kwargs={"account_service": account_service})
    api.add_resource(AccountUpdate, "/accounts/<int:id>", resource_class_kwargs={"account_service": account_service})
    api.add_resource(AccountDelete, "/accounts/<int:id>", resource_class_kwargs={"account_service": account_service})
    
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create database tables for our data models
        migrate.init_app(app, db)
      

    return app
