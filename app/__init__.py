from flask import Flask, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from app.settings import API_v1
from app.config import app_config
from flask_jwt_extended import JWTManager




db = SQLAlchemy()

def create_app(config_name):

	#db connection


	app = Flask(__name__)
	api = Api(app)

	app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['JWT_BLACKLIST_ENABLED'] = True
	app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

	jwt = JWTManager(app) # not creating /auth


	"""
	@jwt.user_claims_loader
	def add_claims_to_jwt(identity):
		from user.models import User
		if identity == 1 : #instead of hard-coding, you should read from a config or database
			return { 'is_admin': True }
		return { 'is_admin': False }
		"""
	@jwt.token_in_blacklist_loader
	def check_if_token_in_blacklist(decrypted_token):
		from user.models import User
		from blacklist.models import TokenBlacklist

		return decrypted_token['jti'] in TokenBlacklist.get_all()

	@jwt.expired_token_loader
	def expired_token_callback():
		from user.models import User
		return jsonify({
		'description': 'The token has expired',
		'error': 'token_expired'
		}), 401

	@jwt.invalid_token_loader
	def invalid_token_callback(error):
		from user.models import User
		return jsonify({
		'description': 'Signature verification failed.',
		'error': 'invalid_token'
		}), 401

	@jwt.unauthorized_loader
	def missing_token_callback(error):
		from user.models import User
		return jsonify({
		'description': 'Request does not contain an access token.',
		'error': 'authorization_required'
		}), 401

	@jwt.needs_fresh_token_loader
	def token_not_fresh_callback():
		from user.models import User
		return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    	}), 401


	@jwt.revoked_token_loader
	def revoked_token_callback():
		from user.models import User
		return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    	}), 401



	#resource import area


	from todo.resources import TodoListsApi, TodoListApi
	api.add_resource(TodoListsApi, API_v1 + '/todolists')
	api.add_resource(TodoListApi, API_v1 + '/todolist', API_v1 + '/todolist/<string:id>')

	from shopping.resources import ShoppingListsAPI, ShoppingListAPI
	api.add_resource(ShoppingListsAPI, API_v1 + '/shoppinglists')
	api.add_resource(ShoppingListAPI, API_v1 + '/shoppinglist', API_v1 + '/shoppinglist/<string:id>')

	from user.resources import (
			UserRegisterAPI,
			UserAPI,
			UserLoginAPI,
			UserLogoutAPI,
			TokenRefreshAPI
	)
	api.add_resource(UserRegisterAPI, API_v1 + '/register')
	api.add_resource(UserAPI, API_v1 + '/user/<string:id>')
	api.add_resource(UserLoginAPI, API_v1 + '/login')
	api.add_resource(UserLogoutAPI, API_v1 + '/logout')
	api.add_resource(TokenRefreshAPI, API_v1 + '/refresh')


	db.init_app(app)
	return app
