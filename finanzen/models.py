from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Revenue(db.Model):
	__tablename__ = 'revenues'

	einnahmenID = db.Column(db.Integer, primary_key=True)
	haushalt_id = db.Column(db.Integer, db.ForeignKey('haushalt.haushaltID'))




class Expenditure(db.Model):
	__tablename__ =  'expenditure'

	ausgabenID = db.Column(db.Integer, primary_key=True)
	haushalt_id = db.Column(db.Integer, db.ForeignKey('haushalt.haushaltID'))

class Haushalt(db.Model):
	__tablename__ = 'haushalt'

	haushaltID = db.Column(db.Integer, primary_key=True)
	id = db.Column(UUID(as_uuid=True), default=lambda: uuid.uuid4(), unique=True)

	users = db.relationship('User', backref='Haushalt', lazy=False)
	einnahmen = db.relationship('Revenue', backref='Haushalt', lazy=False)
	ausgaben = db.relationship('Expenditure', backref='Haushalt', lazy=False)
