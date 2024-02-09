from flask_restful import Resource, request
from flask import jsonify

class DepositCreate(Resource):
  def __init__(self, **kwargs):
    self.transaction_service = kwargs['transaction_service']
  
  def post(self):
    data = request.get_json()
    if not data or not data.get("account_id") or not data.get("amount"):
        return jsonify({"message": "Missing information"}), 400
    
    account_id = data.get("account_id")
    amount = data.get("amount")
    success, message = self.transaction_service.make_deposit(account_id, amount)
    
    if success:
        return jsonify({'message': 'Deposit successful'}), 201
    else:
        return jsonify({'message': message}), 400

class TransferCreate(Resource):
  def __init__(self, **kwargs):
    self.transaction_service = kwargs['transaction_service']
  
  def post(self):
    data = request.get_json()
    if not data or not data.get("from_account_id") or not data.get("recipient_account_id") or not data.get("amount"):
        return jsonify({"message": "Missing information"}), 400
    
    sender_account = data.get("sender_account_id")
    recipient_account = data.get("recipient_account_id")
    amount = data.get("amount")
    success, message = self.transaction_service.make_transfer(sender_account, recipient_account, amount)
    
    if success:
      return jsonify({'message': 'Transfer successful'}), 201
    else:
      return jsonify({'message': message}), 400
