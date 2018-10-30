from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from app.settings import API_v1
from app.config import app_config
db = SQLAlchemy()

def create_app(config_name):

	#db connection


	app = Flask(__name__)
	api = Api(app)

	app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



	#resource import area


	from todo.resources import TodoListsApi, TodoListApi
	api.add_resource(TodoListsApi, API_v1 + '/todolists')
	api.add_resource(TodoListApi, API_v1 + '/todolist', API_v1 + '/todolist/<int:id>')

	from shopping.resources import ShoppingListsAPI, ShoppingListAPI
	api.add_resource(ShoppingListsAPI, API_v1 + '/shoppinglists')
	api.add_resource(ShoppingListAPI, API_v1 + '/shoppinglist', API_v1 + '/shoppinglist/<string:id>')

	db.init_app(app)
	return app
