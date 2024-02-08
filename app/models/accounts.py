from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db
from flask_validator import  ValidateNumber

class Account(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    account_number = db.Column(db.Numeric(20), unique=True, nullable=False)
    account_type = db.Column(db.String(50), nullable=False)  #savings, checking
    balance = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(50), nullable=False, default="active")
    date_opened = db.Column(db.DateTime, default=datetime.utcnow)
    date_closed = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # user = db.relationship('User', back_populates='account')
    # transactions = db.relationship('Transaction', back_populates='account', foreign_keys='[Transaction.account_id]')
    
    @classmethod
    def __declare_last__(cls):
        ValidateNumber(
            Account.account_number, True, True, "The account number must be a number"
        )  # True => Allow internationalized addresses, True => Check domain name resolution.
        

    def to_dict(self):
        return {
            "id": self.id,
            "account_number": self.name,
            "account_type": self.email,
            "balance": self.mobile_number,
            "user_id": self.user_id,
            "status": self.status,
            "date_opened": self.date_opened,
            "date_closed": self.date_closed,
        }
