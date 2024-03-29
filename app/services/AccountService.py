from datetime import datetime
import random
from app.models.accounts import Account
from app.db.database import db
from app.models.transactions import Transaction


class AccountService:
  def create_account(self, account_type: str,  balance : float, status: str, user_id: int):
    # call generate function
    account_number = self.generate_account_number()
    
    new_account = Account(account_number=account_number, account_type=account_type, balance=balance, status=status,  user_id=user_id)
    db.session.add(new_account)
    db.session.commit()
    return new_account
  
  def generate_account_number(self):
    while True:
      now = datetime.utcnow()
      random_number = random.randint(1000, 9999)
      account_number = int(now.strftime("%Y%m%d%")[:-3] + str(random_number))
      # validated if account number is unique
      if not Account.query.filter_by(account_number=account_number).first():
        return account_number
      else: 
        return {'message': 'Account number already exists'}, 400

      
  def get_account_detail(self, id=None):
    return Account.query.get(id)

  def get_account_detail_by_user(self, user_id=None):
    return Account.query.filter_by(user_id=user_id).first()

  def get_accounts(self):
    return Account.query.all()
  
  def get_accounts_by_user(self, user_id=None):
    return Account.query.filter_by(user_id=user_id).all()
  
  def get_account_by_account_number(self, account_number=None):
    return Account.query.filter_by(account_number=account_number).first()
  
  def update_account(self, id=None, data=None):
    account = Account.query.get(id)
    if not account:
        return {'message': 'Account not found'}, 404
    print('dataUpdateAccount', data)
    account.account_type = data.get('account_type', account.account_type)
    account.balance = data.get('balance', account.balance)
    account.account_number = data.get('account_number', account.account_number)
    account.status = data.get('status', account.status)
    db.session.commit()

    return account, {'message': 'Account updated successfully'}, 200
    
  def delete_account(self, id=None):
    account = Account.query.get(id)
    if not account:
      return {'message': 'Account not found'}, 404
    if account.balance > 0:
      return {'message': 'Account has a balance greater than 0. Cannot delete account'}, 400
    
    transactions = Transaction.query.filter_by(account_id=id).first()
    if transactions:
      return {'message': 'Account has transactions. Cannot delete account'}, 400
    
    db.session.delete(account)
    db.session.commit()
    return {'message': 'Account deleted successfully'}, 200