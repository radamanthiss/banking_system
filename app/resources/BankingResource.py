from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

class DepositCreate(Resource):
  def __init__(self, **kwargs):
    self.transaction_service = kwargs['transaction_service']

  @jwt_required()
  def post(self):
    data = request.get_json()
    if not data or not data.get("account_id") or not data.get("amount"):
        return {"message": "Missing information"}, 400
    
    account_id = data.get("account_id")
    amount = data.get("amount")
    description = data.get("description")
    success, message = self.transaction_service.make_deposit(account_id, amount, description)
    
    if success:
        return {'message': 'Deposit successful'}, 201
    else:
        return {'message': message}, 400

class TransferCreate(Resource):
  def __init__(self, **kwargs):
    self.transaction_service = kwargs['transaction_service']

  def post(self):
    data = request.get_json()
    if not data or not data.get("sender_account_id") or not data.get("recipient_account_id") or not data.get("amount"):
        return {"message": "Missing information"}, 400
    
    sender_account = data.get("sender_account_id")
    recipient_account = data.get("recipient_account_id")
    amount = data.get("amount")
    success, message = self.transaction_service.make_transfer(sender_account, recipient_account, amount)
    
    if success:
      return {'message': 'Transfer successful'}, 201
    else:
      return {'message': message}, 400

class WithdrawCreate(Resource):
  def __init__(self, **kwargs):
    self.transaction_service = kwargs['transaction_service']
  
  def post(self):
    data = request.get_json()
    if not data or not data.get("account_id") or not data.get("amount"):
        return {"message": "Missing information"}, 400
    
    account_id = data.get("account_id")
    amount = data.get("amount")
    description = data.get("description")
    success, message = self.transaction_service.make_withdrawal(account_id, amount, description)
    
    if success:
      return {'message': 'Withdrawal successful'}, 201
    else:
      return {'message': message}, 400

class TransactionListByUser(Resource):
  def __init__(self, **kwargs):
    self.transaction_service = kwargs['transaction_service']
  
  def get(self, user_id):
    transactions = self.transaction_service.get_transactions_by_user(user_id)
    return {
      "transactions": [
        {
          "id": transaction.id,
          "transaction_type": transaction.transaction_type,
          "amount": transaction.amount,
          "description": transaction.description,
          "account_id": transaction.account_id,
          "user_id": transaction.user_id,
          "created_at": str(transaction.created_at),
        }
        for transaction in transactions
      ]
    }, 200