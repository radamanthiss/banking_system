from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db
from flask_validator import ValidateEmail, ValidateString, ValidateNumber
from werkzeug.security import generate_password_hash, check_password_hash

from app.schemas.UserSchema import UserSchema

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(60), nullable=False, default="client")
    mobile_number = db.Column(db.Numeric(10), unique=True, nullable=False)
    country = db.Column(db.String(60), nullable=False)
    document_number = db.Column(db.Numeric(10), unique=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def __declare_last__(cls):
        ValidateEmail(
            User.email, True, True, "The email is not valid. Please check it"
        )  # True => Allow internationalized addresses, True => Check domain name resolution.
        ValidateString(User.name, True, True, "The username type must be string")
        ValidateNumber(
            User.mobile_number, True, True, "The mobile number type must be number"
        )
        ValidateNumber(
            User.document_number, True, True, "The document number type must be number"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "document_number": str(int(self.document_number)),
            "name": self.name,
            "email": self.email,
            "mobile_number": str(int(self.mobile_number)),
            "user_type": self.user_type,
            "country": self.country,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    # def __str__(self):
    #     return f'id: {self.id}, name: {self.name}, email: {self.email}, mobile_number: {self.mobile_number}, user_type: {self.user_type}, country: {self.country}, created_at: {self.created_at}, updated_at: {self.updated_at}'