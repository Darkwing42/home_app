from flask_restful import Resource
from flask import request
from datetime import datetime
from shopping.models import ShoppingItemModel, ShoppinglistModel
from user.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity,fresh_jwt_required
from sqlalchemy import and_


class ShoppingListsAPI(Resource):
	@jwt_required
	def get(self):
		
		user = User.find_by_id(get_jwt_identity())

		shopLists = ShoppinglistModel.get_all_by_user(user.userID)

		return {'shoppingLists': [shopList.json() for shopList in shopLists]}, 201

class ShoppingListAPI(Resource):
    
	@jwt_required
	def get(self, list_id):
		data = request.get_json()
		user = User.find_by_id(get_jwt_identity())
		
		shoppingList = ShoppinglistModel.query.filter(and_(ShoppinglistModel.id == list_id, ShoppinglistModel.user_id == user.userID)).first()

		return {'shoppingList': shoppingList.json() }, 201
		
	@fresh_jwt_required	
	def post(self):
		data = request.get_json()
		user = User.find_by_id(get_jwt_identity())
		
		shoppingList = ShoppinglistModel(data['shoppinglist_name'], data['shoppinglist_done'], user.userID)
		
		items = []
		for item in data['shoppingItems']:
			obj = ShoppingItemModel(item['item_name'], item['item_quantity'])
			items.append(obj)

		shoppingList.shoppingItems = items

		shoppingList.save()

		return {'message': 'Data successfully saved'}, 201
		

		
	
	def put(self, id):
		pass
	
		
