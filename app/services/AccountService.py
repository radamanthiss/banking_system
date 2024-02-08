from flask import jsonify
from app.models.accounts import Account
from app.db.database import db


class AccountService:
  def create_account(self, account_number: int, account_type: str,  balance : float, status: str, user_id: int):
    account = Account.query.filter_by(account_number=account_number).first()
    if account:
      return jsonify({'message': 'Account number already exists'}), 400
    else:
      new_account = Account(account_number=account_number, account_type=account_type, balance=balance, status=status,  user_id=user_id)
      db.session.add(new_account)
      db.session.commit()
      return new_account
      
  def get_account_detail(self, id=None):
    return Account.query.get(id)

  def get_accounts(self):
    return Account.query.all()
  
  def update_account(self, id=None, data=None):
    account = Account.query.get(id)
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    account.name = data.get('name', account.name)
    account.email = data.get('email', account.email)
    account.mobile_number = data.get('mobile_number', account.mobile_number)
    account.country = data.get('country', account.country)
    db.session.commit()

    return jsonify({'message': 'Account updated successfully'}), 200
    
  def delete_account(self, id=None):
    account = Account.query.get(id)
    if not account:
      return jsonify({'message': 'Account not found'}), 404
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': 'Account deleted successfully'}), 200