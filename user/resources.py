from flask_restful import Resource
from user.models import User
from app.utils.uuid_converter import str2uuid
from flask_jwt_extended import (
		create_access_token,
		create_refresh_token,
		jwt_refresh_token_required,
		get_jwt_identity,
		jwt_required,
		get_raw_jwt
)
from flask import request
from blacklist.models import TokenBlacklist
import bcrypt
from app.utils import crossdomain

class UserRegisterAPI(Resource):
	
    def post(self):
        data = request.get_json()
	

        if User.find_by_username(data['username']):
            return {'message': "A user with this username already exists"}, 400
		
        if not User.query.all() :
            user = User(**data)
            user.is_admin = True
            user.save()
            return {"message": "Admin successfully created"}, 201
        else:
            user = User(**data)
            user.is_admin = False
            user.save()
            return {'message': "User successfully created"}, 201

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
		print(data)
		#find user in the database
		user = User.find_by_username(data['username'])
        #check password
		if user and user.check_password(data['password'], user._password):
			access_token = create_access_token(identity=str(user.id), fresh=True)
			refresh_token = create_refresh_token(identity=str(user.id))
			return {
                'user_id': str(user.id),
				'access_token': access_token,
				'refresh_token': refresh_token
				}, 200

		return {"message": "Invalid credentials", "data": data }, 401

class UserLogoutAPI(Resource):

	@jwt_required
	def post(self):
		jti = get_raw_jwt()['jti']
		token = TokenBlacklist(jti=jti)
		token.save()
		return {'message': 'Successfully logged out'}, 200



class TokenRefreshAPI(Resource):
	@jwt_refresh_token_required
	def post(self):
		current_user = get_jwt_identity()
		new_token = create_access_token(identity=current_user, fresh=False)
		return { 'access_token': new_token }, 200
