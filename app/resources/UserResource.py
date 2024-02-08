from flask_restful import Resource, request, Api
from flask import Flask, jsonify
from app.models.users import User
from app.services.UserService import UserService


class UserCreate(Resource):
  def __init__(self, **kwargs):
    self.user_service = kwargs['user_service']
  
  def post(self):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    mobile_number = data.get("mobile_number")
    country = data.get("country")
    user = self.user_service.create_user(name, email, mobile_number, country)
    return {'id': user.id}, 201

class UserDetail(Resource): 
  def __init__(self, **kwargs):
    self.user_service = kwargs['user_service']
    
  def get(self, id=None):
    user = self.user_service.get_user_detail(id)
    if user:
      return {
        "user": {
          "id": user.id,
          "name": user.name,
          "email": user.email,
          "mobile_number": int(user.mobile_number),
        }
      }, 200
    return jsonify({"message": "User not found"}), 404

class UserList(Resource):
  def __init__(self, **kwargs):
    self.user_service = kwargs['user_service']
    
  def get(self):
    users = self.user_service.get_users()
    return {
      "users": [
        {
          "id": user.id,
          "name": user.name,
          "email": user.email,
          "mobile_number": int(user.mobile_number),
        }
        for user in users
      ]
    }, 200

class UserUpdate(Resource):
  def __init__(self, **kwargs):
    self.user_service = kwargs['user_service']
    
  def put(self, id):
    data = request.get_json()
    user = self.user_service.update_user(id, data)
    return jsonify({
      "user": {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "mobile_number": int(user.mobile_number),
      }
    }), 200

class UserDelete(Resource):
  def __init__(self, **kwargs):
    self.user_service = kwargs['user_service']
    user = self.user_service.delete_user(id)
  
  def delete(self, id):
    self.user_service.delete_user(id)
    return jsonify({"message": "User deleted successfully"}), 200