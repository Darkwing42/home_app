from app import db
from flask_restful import Resource
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.utils.uuid_converter import str2uuid

class TokenBlacklist(db.Model):
    __tablename__ = 'tokenblacklist'

    tokenblacklistID = db.Column(db.Integer, primary_key=True)
    id = db.Column(UUID(as_uuid=True), default=lambda: uuid.uuid4(), unique=True)
    jti = db.Column(db.String())

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_jti(cls):
        return cls.query.filter_by(jti=jti).all()
