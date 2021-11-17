"""DATS configuration table
"""
from app.extensions import db


class ConfigTable(db.Model):

    __tablename__ = 'Config'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), nullable=False, unique=True)
    value = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value
        }
