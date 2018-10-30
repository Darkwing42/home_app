from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Einnahme(db.Model):
	__tablename__ = 'einnahmen'

	einnahmenID = db.Column(db.Integer, primary_key=True)
	haushalt_id = db.Column(db.Integer, db.ForeignKey('haushalt.haushaltID'))
	



class Ausgabe(db.Model):
	__tablename__ =  'ausgaben'

	ausgabenID = db.Column(db.Integer, primary_key=True)
	haushalt_id = db.Column(db.Integer, db.ForeignKey('haushalt.haushaltID'))
	
class Haushalt(db.Model):
	__tablename__ = 'haushalt'

	haushaltID = db.Column(db.Integer, primary_key=True)	
	id = db.Column(UUID(as_uuid=True, default=lambda: uuid.uuid4().hex), unique=True)
	users = db.relationship('User', backref='Haushalt', lazy=False)
	einnahmen = db.relationship('Einnahme', backref='Haushalt', lazy=False)
	ausgaben = db.relationship('Ausgabe', backref='Haushalt', lazy=False)


