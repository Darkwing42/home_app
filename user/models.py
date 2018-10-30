from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
import bcrypt

class UserSettings(db.Model):
	__tablename__ =  'usersettings'

	userSettingsID = db.Column(db.Integer, primary_key=True)
	id = db.Column(UUID(as_uuid=True, default=lambda: uuid.uuid4().hex), unique=True)
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
	id = db.Column(UUID(as_uuid=True, default=lambda: uuid.uuid4().hex), unique=True)
	username = db.Column(db.String(120), nullable=False, unique=True)
	email = db.Column(db.String, unique=True, nullable=False)
	authenticated = db.Column(db.Boolean, default=False)

	_password = db.Column(db.String(255), nullable=False)
	
	settings = db.relationship('UserSettings', backref='User', lazy=False)
	haushalt_id = db.Column(db.Integer, db.ForeignKey('haushalt.haushaltID'))

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password
		self.authenticated = False
	
	

			
	def hash_password(self, password):
		return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
	
	def check_password(self, password, hashed_pw):
		return bcrypt.checkpw(password, hashed_pw)


	
