from flask_restful import Resource
from flask import request
from datetime import datetime
from shopping.models import ShoppingItemModel, ShoppinglistModel
from user.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

class ShoppingListsAPI(Resource):
	@jwt_required
	def get(self):
		
		user = User.find_by_id(get_jwt_identity())

		shopLists = ShoppinglistModel.get_all_by_user(user.userID)

		return {'shoppingLists': [shopList.json() for shopList in shopLists]}, 201

class ShoppingListAPI(Resource):

	def get(self, list_id):
		data = request.get_json()

		shoppingList = ShoppinglistModel.get_by_id(id)
		if shoppingList is None:
			return {'message': 'No data found'}, 500
		else:
			return {'shoppinglist': shoppingList.json()}, 201
			
		
	@jwt_required	
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
	
		
