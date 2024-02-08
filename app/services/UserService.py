from flask import jsonify
from app.models.users import User
from app.db.database import db


class UserService:
  def create_user(self, name: str, email: str, mobile_number: int, country: str):
    new_user = User(name=name, email=email, mobile_number=mobile_number, country=country)
    db.session.add(new_user)
    db.session.commit()
    return new_user
      
  def get_user_detail(self, id=None):
    return User.query.get(id)

  def get_users(self):
    return User.query.all()
  
  def update_user(self, id=None, data=None):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.mobile_number = data.get('mobile_number', user.mobile_number)
    user.country = data.get('country', user.country)
    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200
    
  def delete_user(self, id=None):
    user = User.query.get(id)
    if not user:
      return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200