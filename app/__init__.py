from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from app.settings import API_v1
from app.config import app_config
from user.models import User


db = SQLAlchemy()

def create_app(config_name):

	#db connection


	app = Flask(__name__)
	api = Api(app)

	app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


	jwt = JWTManager(app) # not creating /auth

	@jwt.user_claims_loader
	def add_claims_to_jwt(identity):
		if User.check_is_admin(identity) : #instead of head-coding, you should read from a config or database
			return { 'is_admin': True }
		return { 'is_admin': False }

	


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
			TokenRefreshAPI
	)
	api.add_resource(UserRegisterAPI, API_v1 + '/register')
	api.add_resource(UserAPI, API_v1 + '/user/<string:id>')
	api.add_resource(UserLoginAPI, API_v1 + '/login')
	api.add_resource(TokenRefreshAPI, API_v1 + '/refresh')


	db.init_app(app)
	return app
