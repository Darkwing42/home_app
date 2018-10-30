from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class ShoppingItemModel(db.Model):
	__tablename__ = 'shoppingItems'

	id = db.Column(UUID(as_uuid=True), default=lambda: uuid.uuid4().hex)
	internal_id = db.Column(db.Integer, primary_key=True)
	shoppingItem_name = db.Column(db.String(200))
	shoppingItem_quantity = db.Column(db.Integer)
	shoppingItem_done = db.Column(db.Boolean, default=False)
	shoppingList_id = db.Column(db.Integer, db.ForeignKey('shoppinglists.internal_id'))

	def __init__(self, name, quantity):
		self.shoppingItem_name = name
		self.shoppingItem_quantity = quantity


	def json(self):
		return {
	"id": str(self.id),
	"shoppingItem_name": self.shoppingItem_name,
	"shoppingItem_quantity": self.shoppingItem_quantity,
	"shoppingItem_done": self.shoppingItem_done,
	"shoppingList_id": self.shoppingList_id
				}

	def save(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()


class ShoppinglistModel(db.Model):
	__tablename__ = 'shoppinglists'

	id = db.Column(UUID(as_uuid=True), default=lambda: uuid.uuid4().hex)
	internal_id = db.Column(db.Integer, primary_key=True)
	shoppinglist_name = db.Column(db.String(120))
	shoppinglist_done = db.Column(db.Boolean, default=False)
	shoppingItems = db.relationship('ShoppingItemModel', backref='ShoppinglistModel', lazy=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.userID'))

	def __init__(self, name, done):
		self.shoppinglist_name = name
		self.shoppinglist_done = done


	def json(self):
		return {
	"id": str(self.id),
	"shoppinglist_name": self.shoppinglist_name,
	"shoppinglist_done": self.shoppinglist_done,
	"shoppingItems": [ item.json() for item in self.shoppingItems ]
	}

	def save(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def get_all(cls):
		return cls.query.all()

	@classmethod
	def get_by_id(cls, id):
		return cls.query.filter_by(id=id).first()
