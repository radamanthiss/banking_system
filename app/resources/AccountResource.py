from flask_restful import Resource, request, Api
from app.models.accounts import Account
from app.services.AccountService import AccountService


class AccountCreate(Resource):
  def __init__(self, **kwargs):
    self.account_service = kwargs['account_service']
  
  def post(self):
    data = request.get_json()
    account_number = int(data.get("account_number"))
    account_type = data.get("account_type")
    balance = data.get("balance")
    status = data.get("status")
    user_id = data.get("user_id")
    account = self.account_service.create_account(account_number, account_type, balance, status, user_id)
    
    return {'account_number': int(account.account_number)}, 201

class AccountDetail(Resource): 
  def __init__(self, **kwargs):
    self.account_service = kwargs['account_service']
    
  def get(self, id=None):
    account = self.account_service.get_account_detail(id)
    if account:
      return {
        "account": {
          "id": account.id,
          "account_number": int(account.account_number),
          "account_type": account.account_type,
          "user_id": account.user_id,
          "balance": float(account.balance),
          "status": account.status,
          "date_opened": account.date_opened.strftime("%Y-%m-%d"),
          "date_closed": account.date_closed if account.date_closed else "Not closed yet"
        }
      }, 200
    return {"message": "User not found"}, 404

class AccountDetailByAccountNumber(Resource):
  def __init__(self, **kwargs):
    self.account_service = kwargs['account_service']
    
  def get(self, account_number=None):
    account = self.account_service.get_account_by_account_number(account_number)
    if account:
      return {
        "account": {
          "id": account.id,
          "account_number": int(account.account_number),
          "account_type": account.account_type,
          "user_id": account.user_id,
          "balance": float(account.balance),
          "status": account.status,
          "date_opened": account.date_opened.strftime("%Y-%m-%d"),
          "date_closed": account.date_closed if account.date_closed else "Not closed yet"
        }
      }, 200
    return {"message": "Account not found"}, 404
class AccountDetailByUser(Resource): 
  def __init__(self, **kwargs):
    self.account_service = kwargs['account_service']
    
  def get(self, user_id=None):
    account = self.account_service.get_account_detail_by_user(user_id)
    if account:
      return {
        "account": {
          "id": account.id,
          "account_number": int(account.account_number),
          "account_type": account.account_type,
          "user_id": account.user_id,
          "balance": float(account.balance),
          "status": account.status,
          "date_opened": account.date_opened.strftime("%Y-%m-%d"),
          "date_closed": account.date_closed if account.date_closed else "Not closed yet"
        }
      }, 200
    return {"message": "User not found"}, 404

class AccountList(Resource):
  def __init__(self, **kwargs):
    self.account_service = kwargs['account_service']
    
  def get(self):
    accounts = self.account_service.get_accounts()
    return {
      "accounts": [
        {
         "id": account.id,
          "account_number": int(account.account_number),
          "account_type": account.account_type,
          "user_id": account.user_id,
          "balance": float(account.balance),
          "status": account.status,
          "date_opened": account.date_opened.strftime("%Y-%m-%d") if account.date_opened else "Not opened yet",
          "date_closed": account.date_closed if account.date_closed else "Not closed yet"
        }
        for account in accounts
      ]
    }, 200
    
class AccountListByUser(Resource):
  def __init__(self, **kwargs):
    self.account_service = kwargs['account_service']
    
  def get(self, user_id):
    accounts = self.account_service.get_accounts_by_user(user_id)
    return {
      "accounts": [
        {
          "id": account.id,
          "account_number": int(account.account_number),
          "account_type": account.account_type,
          "user_id": account.user_id,
          "balance": float(account.balance),
          "status": account.status,
          "date_opened": account.date_opened.strftime("%Y-%m-%d") if account.date_opened else "Not opened yet",
          "date_closed": account.date_closed if account.date_closed else "Not closed yet"
        }
        for account in accounts
      ]
    }, 200

class AccountUpdate(Resource):
  def __init__(self, **kwargs):
    self.account_service = kwargs['account_service']
    
  def put(self, id):
    data = request.get_json()
    account, response, status = self.account_service.update_account(id, data)
    if not account:
      return response, status
    
    return {
      "account": {
        "id": account.id,
        "account_number": int(account.account_number),
        "account_type": account.account_type,
        "user_id": account.user_id,
        "balance": float(account.balance),
        "status": account.status,
        "date_opened": account.date_opened.strftime("%Y-%m-%d") if account.date_opened else "Not opened yet",
      },
      "message": response['message']
    }, status

class AccountDelete(Resource):
  def __init__(self, **kwargs):
    self.account_service = kwargs['account_service']
  
  def delete(self, id):
    self.account_service.delete_account(id)
    return {"message": "User deleted successfully"}, 200