import json
from flask_jwt_extended import create_access_token
from flask_restful import Resource, request, Api
from flask import Flask, jsonify
from app.models.users import User
from app.services.UserService import UserService


class UserCreate(Resource):
  def __init__(self, **kwargs):
    self.user_service = kwargs['user_service']
  
  def post(self):
    data = request.get_json()
    if not data or not data.get("name") or not data.get("email") or not data.get("mobile_number") or not data.get("country") or not data.get("password") or not data.get("user_type"):
      return jsonify({"message": "Missing information"}), 400
    if self.user_service.get_user_by_email(data.get("email")):
      return jsonify({"message": "Email already exists"}), 400
    
    name = data.get("name")
    email = data.get("email")
    mobile_number = data.get("mobile_number")
    country = data.get("country")
    user_type = data.get("user_type")
    password = data.get("password")
    user = self.user_service.create_user(name, email, password, mobile_number, country, user_type)
    return {'id':user.id, "message":"User successfully registered"}, 201

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

class UserLogin(Resource):
  def __init__(self, **kwargs):
    self.user_service = kwargs['user_service']
    
  def post(self):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user, error = self.user_service.verify_password(email, password)
    
    if user:  
      # Assuming you have a method to generate auth tokens or similar
      # token = generate_auth_token(user.id)
      access_token = create_access_token(identity=user.id)
      user_data = user.to_dict() if hasattr(user, 'to_dict') else {}
      return {
          'message': 'User logged in successfully',
          'user':user_data,
          'access_token': access_token,
      },
    else:
      return {'message': error}, 401