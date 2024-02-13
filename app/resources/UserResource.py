import json
from flask_jwt_extended import create_access_token
from flask_restful import Resource, request, Api
from app.models.users import User
from app.services.UserService import UserService


class UserCreate(Resource):
  def __init__(self, **kwargs):
    self.user_service = kwargs['user_service']
  
  def post(self):
    data = request.get_json()
    if not data or not data.get("name") or not data.get("email") or not data.get("mobile_number") or not data.get("country") or not data.get("password") or not data.get("user_type") or not data.get("document_number"):
      return {"message": "Missing information"}, 400
    if self.user_service.get_user_by_email(data.get("email")):
      return {"message": "Email already exists"}, 400
    
    name = data.get("name")
    email = data.get("email")
    mobile_number = data.get("mobile_number")
    country = data.get("country")
    user_type = data.get("user_type")
    password = data.get("password")
    document_number = data.get("document_number")
    user = self.user_service.create_user(name, email, password, mobile_number, country, user_type, document_number)
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
          "country": user.country,
          "document_number": int(user.document_number),
          "user_type": user.user_type,
          "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
      }, 200
    return {"message": "User not found"}, 404

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
          "country": user.country,
          "document_number": int(user.document_number),
          "user_type": user.user_type,
          "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for user in users
      ]
    }, 200

class UserUpdate(Resource):
  def __init__(self, **kwargs):
    self.user_service = kwargs['user_service']
    
  def put(self, id):
    data = request.get_json()
    user, response, status = self.user_service.update_user(id, data)
    if not user:
      return response, status
    
    return {
      "user": {
        "id": int(user.id),
        "name": user.name,
        "email": user.email,
        "mobile_number": int(user.mobile_number),
        "country": user.country,
        "user_type": user.user_type,
      },
      "message": response['message']
    }, status

class UserDelete(Resource):
  def __init__(self, **kwargs):
    self.user_service = kwargs['user_service']
    # user = self.user_service.delete_user(id)
  
  def delete(self, id):
    response = self.user_service.delete_user(id)
    return response

class UserLogin(Resource):
  def __init__(self, **kwargs):
    self.user_service = kwargs['user_service']
    
  def post(self):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user, error = self.user_service.verify_password(email, password)
    
    if user:
      access_token = create_access_token(identity=user.id)
      user_data = user.to_dict() if hasattr(user, 'to_dict') else {}
      return {
          'message': 'User logged in successfully',
          'user':user_data,
          'access_token': access_token,
      },
    else:
      return {'message': error}, 401
    
class UserDetailByDocument(Resource):
  def __init__(self, **kwargs):
    self.user_service = kwargs['user_service']
  
  def get(self, document_number):
    user = self.user_service.get_user_by_document_number(document_number)
    if user:
      return {
        "user": {
          "id": user.id,
          "name": user.name,
          "email": user.email,
          "mobile_number": int(user.mobile_number),
          "country": user.country,
          "document_number": int(user.document_number),
          "user_type": user.user_type,
          "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
      }, 200
    return {"message": "User not found"}, 404