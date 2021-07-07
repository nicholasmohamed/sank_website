from flask import current_app
from app import db
from sqlalchemy.dialects.mysql import TIME


# database container for sankchewaire merchandise
class SankMerchDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    price = db.Column(db.Integer, index=True)
    imageLink = db.Column(db.String(256), index=True)
    description = db.Column(db.String(256), index=True)
    quantity = db.Column(db.Integer, index=True)
    isAvailable = db.Column(db.Boolean, index=True)

    def __repr__(self):
        return '<SankMerchDb {}>'.format(self.message)
