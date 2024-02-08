from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db
from flask_validator import ValidateNumber

class Transaction(db.Model):
    __tablename__ = "transaction"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # e.g., deposit, withdrawal
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    recipient_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # account = db.relationship('Account', back_populates='transaction', foreign_keys=[account_id])
    # recipient_account = db.relationship('Account', foreign_keys=[recipient_account_id])
    # user = db.relationship('User', back_populates='transaction')
    
    @classmethod
    def __declare_last__(cls):
        ValidateNumber(
            Transaction.amount, True, True, "The account number must be a number"
        )  # True => Allow internationalized addresses, True => Check domain name resolution.
        

    def to_dict(self):
        return {
            "id": self.id,
            "transaction_type": self.name,
            "amount": self.email,
            "description": self.mobile_number,
            "user_id": self.country,
            "created_at": self.status,
            "account_id": self.date_opened,
            "recipient_account_id": self.date_closed,
            "user_id": self.user_id,
        }
