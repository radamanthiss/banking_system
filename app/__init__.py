from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.db.database import db
from flask_restful import Api
from app.resources.BankingResource import DepositCreate, TransactionListByUser, TransferCreate, WithdrawCreate
from app.resources.UserResource import UserCreate, UserDetail, UserDetailByDocument, UserList, UserLogin, UserUpdate, UserDelete
from app.resources.AccountResource import AccountCreate, AccountDetail, AccountDetailByAccountNumber, AccountDetailByUser, AccountList, AccountListByUser, AccountUpdate, AccountDelete
from app.services.AccountService import AccountService
from app.services.UserService import UserService
from app.services.BankingService import TransactionService
from flask_cors import CORS

migrate = Migrate()

def create_app(config=None):
    user_service = UserService()
    account_service = AccountService()
    transaction_service = TransactionService()

    app = Flask(__name__, instance_relative_config=True)    
    if config is None:
        app.config.from_object("config.BaseConfig")
    else:
        app.config.from_object(config)
    api = Api(app)
    jwt = JWTManager(app)
    CORS(app, resources={r"/*": {"origins": ["http://localhost", "https://bank-app-g5en.onrender.com"]}})
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"message": "Token has expired. Please log in again."}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):  # Invalid token string
        return {"message": "Invalid token. Please provide a valid token."}, 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):  # No token provided
        return {"message": "Authorization header is missing. Please provide a token."}, 401

    # Add resources for users
    api.add_resource(UserCreate, "/register", resource_class_kwargs={"user_service": user_service})
    api.add_resource(UserDetail, "/users/<int:id>", resource_class_kwargs={"user_service": user_service})
    api.add_resource(UserList, "/users", resource_class_kwargs={"user_service": user_service})
    api.add_resource(UserUpdate, "/users/<int:id>", resource_class_kwargs={"user_service": user_service})
    api.add_resource(UserDelete, "/users/<int:id>", resource_class_kwargs={"user_service": user_service})
    api.add_resource(UserLogin, "/login", resource_class_kwargs={"user_service": user_service})
    api.add_resource(UserDetailByDocument, "/users/document_number/<int:document_number>", resource_class_kwargs={"user_service": user_service})
    
    # Add resources for accounts
    api.add_resource(AccountCreate, "/accounts", resource_class_kwargs={"account_service": account_service, "user_service": user_service})
    api.add_resource(AccountDetail, "/accounts/<int:id>", resource_class_kwargs={"account_service": account_service})
    api.add_resource(AccountList, "/accounts", resource_class_kwargs={"account_service": account_service})
    api.add_resource(AccountUpdate, "/accounts/<int:id>", resource_class_kwargs={"account_service": account_service})
    api.add_resource(AccountDelete, "/accounts/<int:id>", resource_class_kwargs={"account_service": account_service})
    api.add_resource(AccountDetailByUser, "/accounts/user_id/<int:user_id>", resource_class_kwargs={"account_service": account_service})
    api.add_resource(AccountListByUser, "/accounts/by_user_id/<int:user_id>", resource_class_kwargs={"account_service": account_service})
    api.add_resource(AccountDetailByAccountNumber, "/accounts/account_number/<int:account_number>", resource_class_kwargs={"account_service": account_service})
    # Add resources for transactions
    api.add_resource(DepositCreate, "/transactions/deposit", resource_class_kwargs={"transaction_service": transaction_service})
    api.add_resource(TransferCreate, "/transactions/transfer", resource_class_kwargs={"transaction_service": transaction_service})
    api.add_resource(WithdrawCreate, "/transactions/withdraw", resource_class_kwargs={"transaction_service": transaction_service})
    api.add_resource(TransactionListByUser, "/transactions/user_id/<int:user_id>", resource_class_kwargs={"transaction_service": transaction_service})
    
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create database tables for our data models
        migrate.init_app(app, db)
    return app
