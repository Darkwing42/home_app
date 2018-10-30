from flask_restful import Resource
from flask import request
from datetime import datetime
from shopping.models import ShoppingItemModel, ShoppinglistModel

class ShoppingListsAPI(Resource):
	def get(self):

		shopLists = ShoppinglistModel.get_all()

		return {'shoppingLists': [shopList.json() for shopList in shopLists]}, 201

class ShoppingListAPI(Resource):

	def get(self, id):
		data = request.get_json()

		shoppingList = ShoppinglistModel.get_by_id(id)
		if shoppingList is None:
			return {'message': 'No data found'}, 500
		else:
			return {'shoppinglist': shoppingList.json()}, 201
			
		
		
	def post(self):
		data = request.get_json()
		
		shoppingList = ShoppinglistModel(data['shoppinglist_name'], data['shoppinglist_done'])
		
		items = []
		for item in data['shoppingItems']:
			obj = ShoppingItemModel(item['item_name'], item['item_quantity'])
			items.append(obj)

		shoppingList.shoppingItems = items

		shoppingList.save()

		return {'message': 'Data successfully saved'}, 201
		

		
	
	def put(self, id):
		pass
	
		
