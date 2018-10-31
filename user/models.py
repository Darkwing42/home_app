from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
import bcrypt
from app.utils.uuid_converter import str2uuid

from finanzen.models import *
from todo.models import *
from shopping.models import *


class UserSettings(db.Model):
	__tablename__ =  'usersettings'

	userSettingsID = db.Column(db.Integer, primary_key=True)
	id = db.Column(UUID(as_uuid=True), default=lambda: uuid.uuid4(), unique=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.userID'))

	weather_service = db.Column(db.Boolean, default=False)
	todo_service = db.Column(db.Boolean, default=False)
	shopping_service = db.Column(db.Boolean, default=False)

	def json(self):
		return {
	"id": str(self.id),
	"weather_service": self.weather_service,
	"todo_service": self.todo_service,
	"shopping_service": self.shopping_service
	}



class User(db.Model):
	__tablename__ = 'users'

	userID = db.Column(db.Integer, primary_key=True)
	id = db.Column(UUID(as_uuid=True), default=lambda: uuid.uuid4(), unique=True)
	username = db.Column(db.String(120), nullable=False, unique=True)
	email = db.Column(db.String)
	authenticated = db.Column(db.Boolean, default=False)
	is_admin = db.Column(db.Boolean, default=True)

	active = db.Column(db.Boolean, default=True)

	_password = db.Column(db.Binary(60), nullable=False)

	settings = db.relationship('UserSettings', backref='User', lazy=False)

	todolists = db.relationship('TodoList', backref='User', lazy=False)
	shoppinglists = db.relationship('ShoppinglistModel', backref='User', lazy=False)

	haushalt_id = db.Column(db.Integer, db.ForeignKey('haushalt.haushaltID'))

	def __init__(self, username, password):
		self.username = username
		self._password = self.hash_password(password).encode('utf-8')
		self.authenticated = False

	@classmethod
	def check_is_admin(cls, identity):
		user = User.find_by_id(identity)
		if not user:
			return {'message': 'No user found'}
		return user.is_admin

	@classmethod
	def change_is_admin(cls, user_id):
		user = User.find_by_id(user_id)
		if not user:
			return { 'message': 'User not found'}, 404
		elif not user.is_admin:
			return {'message': 'You have not the permission to change this'}, 403
		user.is_admin = not user.is_admin
		cls.save()
		return {'message': '{} is now an administrator'.format(user.username)}, 201

	@classmethod
	def change_active(cls, user_id):
		user = User.find_by_id(user_id)
		if not user:
			return { 'message': 'User not found'}, 404
		user.active = not user.active
		cls.save()
		return {'message': '{} changed to {}'.format(user.username, user.active)}, 201


	def hash_password(self, password):
		return bcrypt.hashpw(password, bcrypt.gensalt(12))


	def check_password(self, password, hashed_pw):
		return bcrypt.checkpw(password, hashed_pw)

	@classmethod
	def find_by_id(cls, id):
		return User.query.filter_by(id=(str2uuid(id))).first()

	@classmethod
	def find_by_username(cls, username):
		return User.query.filter_by(username=username).first()

	def save(self):
		db.session.add(self)
		db.session.commit()

	def json(self):
		return {
		'id': str(self.id),
		'username': self.username,
		'settings': [ setting.json() for settion in self.settings ]
		}
