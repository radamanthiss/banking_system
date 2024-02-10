from app import db
from datetime import datetime
from app.models.accounts import Account
from app.models.transactions import Transaction

class TransactionService:
  def make_deposit(self, account_id, amount, description="Deposit"):
    account = Account.query.get(account_id)
    if not account or amount <= 0:
        return False, "Invalid account or amount."
    if account and amount > 0:
      account.balance += amount
      transaction = Transaction(transaction_type="deposit", amount=amount, description=description, created_at=datetime.utcnow(), account_id=account_id, user_id=account.user_id)
      db.session.add(transaction)
      db.session.commit()
      return True, "Deposit successful."
    return False, "Deposit failed."

  def make_transfer(self,sender_account_id, recipient_account_id, amount, description="Transfer"):
    sender_account = Account.query.get(sender_account_id)
    recipient_account = Account.query.get(recipient_account_id)
    
    if not sender_account or not recipient_account:
      return False, "Invalid recipient account."
    
    if sender_account.balance < amount:
      return False, "Insufficient balance in sender account."
    
    if sender_account_id == recipient_account_id or amount <= 0:
      return False, "Invalid transfer."
    
    sender_account.balance -= amount
    recipient_account.balance += amount
    
    sender_transaction = Transaction(
      transaction_type="transfer_out",
      amount=amount,
      description=f"Transfer to account {recipient_account.account_number}",
      created_at=datetime.utcnow(),
      account_id=sender_account_id,
      user_id=sender_account.user_id
    )
    recipient_transaction = Transaction(
      transaction_type="transfer_in",
      amount=amount,
      description=f"Transfer from account {sender_account.account_number}",
      created_at=datetime.utcnow(),
      account_id=recipient_account_id,
      user_id=recipient_account.user_id,
      recipient_account_id=recipient_account_id  # Optional: If you want to track the recipient in the transaction
    )
    
    db.session.add(sender_transaction)
    db.session.add(recipient_transaction)
    db.session.commit()
    return True, "Transfer successful."
  
  def make_withdrawal(self, account_id, amount, description="Withdrawal"):
    account = Account.query.get(account_id)
    # Check for a valid account and positive withdrawal amount
    if not account or amount <= 0:
      return False, "Invalid account or amount."
    # Check for sufficient funds
    if account.balance < amount:
      return False, "Insufficient funds for withdrawal."
    # If checks pass, proceed with the withdrawal
    account.balance -= amount  # Decrease the account balance
    transaction = Transaction(
      transaction_type="withdrawal",
      amount=amount,
      description=description,
      created_at=datetime.utcnow(),
      account_id=account_id,
      user_id=account.user_id
    )
    db.session.add(transaction)
    db.session.commit()
    return True, "Withdrawal successful."
  
  
  def get_transactions_by_user(self, user_id):
    return Transaction.query.filter_by(user_id=user_id).all()
    