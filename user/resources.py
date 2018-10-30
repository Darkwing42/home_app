from flask_restful import Resource
from user.models import User
from app.utils.uuid_converter import str2uuid
from flask import request

class UserRegisterAPI(Resource):
    def post(self):
        data = request.get_json()

        if User.find_by_username(data['username']):
            return {'message': "A user with this username already exists"}, 400

        user = User(**data)
        user.save()

        return {"message": "User created successfully"}, 201

class UserAPI(Resource):

    @classmethod
    def get(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def change_active(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.active = !user.active
        user.save()

        return {'message': 'User is inactive'}, 200

class UserLoginAPI(Resource):
    def post(self):
        #get data
        data = request.get_json()
        #find user in the database
        
        #check password
        #create access token
        #create refresh token (later)
        #return them
