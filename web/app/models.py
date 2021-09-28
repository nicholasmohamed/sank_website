from flask import current_app
from app import db
from sqlalchemy.dialects.mysql import TIME

# TODO class for tags, will be handled


# database container for sankchewaire merchandise
class SankMerch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    price = db.Column(db.Integer, index=True)
    imageLink = db.Column(db.String(256), index=True)
    description = db.Column(db.String(256), index=True)
    quantity = db.Column(db.Integer, index=True)
    isAvailable = db.Column(db.Boolean, index=True)
    tags = db.Column(db.String(256), index=True)

    def __repr__(self):
        return '<SankMerch {}>'.format(self.message)