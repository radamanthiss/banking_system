import json
from app.models.users import User
from app.db.database import db
from werkzeug.security import check_password_hash

from app.schemas.UserSchema import UserSchema

class UserService:
  def create_user(self, name: str, email: str, password:str, mobile_number: int, country: str, user_type: str):
    new_user = User(name=name, email=email, mobile_number=mobile_number, country=country, user_type=user_type)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return new_user
      
  def get_user_detail(self, id=None):
    return User.query.get(id)
  
  def get_user_by_email(self, email=None):
    return User.query.filter_by(email=email).first()

  def get_users(self):
    return User.query.all()
  
  def update_user(self, id=None, data=None):
    user = User.query.get(id)
    if not user:
      return {'message': 'User not found'}, 404

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.mobile_number = data.get('mobile_number', user.mobile_number)
    user.country = data.get('country', user.country)
    db.session.commit()

    return user,{'message': 'User updated successfully'}, 200
    
  def delete_user(self, id=None):
    user = User.query.get(id)
    if not user:
      return {'message': 'User not found'}, 404
    db.session.delete(user)
    db.session.commit()
    return {'message': 'User deleted successfully'}, 200
  
  def verify_password(self, email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
      return user,None
    else:
      return None, {'message': 'Invalid email or password'}, 400