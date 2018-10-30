from flask_restful import Resource
from user.models import User
from app.utils.uuid_converter import str2uuid
from flask_jwt_extended import ( 
		create_access_token, 
		create_refresh_token, 
		jwt_refresh_token_required,
		get_jwt_identity
)
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

   
    def get(self, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()


class UserLoginAPI(Resource):
	@classmethod
    def post(cls):
        #get data
        data = request.get_json()
		#find user in the database
		user = User.find_by_username(data['username'])
        #check password
		if user and User.check_password(data['password'], user.password):
			access_token = create_access_token(identity=user.id, fresh=True)
			refresh_token = create_refresh_token(identity=user.id)
			return {
		'access_token': access_token,
		'refresh_token': refresh_token
		}, 200

		return {"message": "Invalid credentials"}, 401

class TokenRefreshAPI(Resource):
	@jwt_refresh_token_required
	def post(self):
		current_user = get_jwt_identity()
		new_token = create_access_token(identity=current_user, fresh=False)
		return { 'access_token': new_token }, 200	
