from .users import User
from .accounts import Account
from .transactions import Transaction
from sqlalchemy.orm import relationship

# User to Account relationship
User.account = relationship('Account', order_by=Account.id, back_populates='user', lazy='dynamic')

# Account to User and Transaction relationships
Account.user = relationship('User', back_populates='account')
Account.transaction = relationship('Transaction', order_by=Transaction.id, back_populates='account', foreign_keys='[Transaction.account_id]', lazy='dynamic')

# Transaction to Account relationship
Transaction.account = relationship('Account', foreign_keys=[Transaction.account_id], back_populates='transaction')
Transaction.recipient_account = relationship('Account', foreign_keys=[Transaction.recipient_account_id])

# Transaction to User relationship
Transaction.user = relationship('User', back_populates='transaction')
User.transaction = relationship('Transaction', back_populates='user', lazy='dynamic')


# # Corrected User to Account relationship to reflect one-to-many
# User.accounts = relationship('Account', order_by=Account.id, back_populates='user', lazy='dynamic')

# # Correct Account to User and Transaction relationships
# Account.user = relationship('User', back_populates='accounts')  # Note the plural 'accounts' to match the User side
# Account.transactions = relationship('Transaction', order_by=Transaction.id, back_populates='account', foreign_keys='[Transaction.account_id]', lazy='dynamic')  # Plural 'transactions' for clarity

# # Transaction to Account relationships remain correctly defined
# Transaction.account = relationship('Account', foreign_keys=[Transaction.account_id], back_populates='transactions')  # Ensure 'transactions' is plural
# Transaction.recipient_account = relationship('Account', foreign_keys=[Transaction.recipient_account_id])

# # Correct Transaction to User relationship
# Transaction.user = relationship('User', back_populates='transactions')  # Ensure 'transactions' is plural to match User side
# User.transactions = relationship('Transaction', back_populates='user', lazy='dynamic')  # Correctly plural
