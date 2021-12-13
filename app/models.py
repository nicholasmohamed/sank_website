from flask import current_app
from app import db
import datetime
from sqlalchemy.dialects.mysql import TIME

# TODO class for tags, will be handled


# database container for SankChewAir-E merchandise
class SankMerch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    price = db.Column(db.Float, index=True)
    imageLink = db.relationship('Image', backref='sank_merch', lazy=True)
    description = db.Column(db.String(256), index=True)
    long_description = db.Column(db.String(512), index=True)
    manufacturing_description = db.Column(db.String(512), index=True)
    care_instructions = db.Column(db.String(512), index=True)
    quantity = db.Column(db.Integer, index=True)
    isAvailable = db.Column(db.Boolean, index=True)
    sizes = db.relationship('Size', backref='sank_merch', lazy=True)
    variations = db.relationship('Variation', backref='sank_merch', lazy=True)
    tags = db.Column(db.String(256), index=True)

    def __repr__(self):
        return '<SankMerch {}>'.format(self.message)


class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    size = db.Column(db.String(256), index=True)
    measurement = db.Column(db.String(256), index=True)
    merch_id = db.Column(db.Integer, db.ForeignKey('sank_merch.id'), nullable=False)


class Variation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('sank_merch.id'), nullable=False)
    color = db.Column(db.String(256), index=True)
    Materials = db.Column(db.String(256), index=True)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    imageLink = db.Column(db.String(256), index=True)
    merch_id = db.Column(db.Integer, db.ForeignKey('sank_merch.id'), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.now())
    purchased_merch = db.relationship('PurchasedMerch', backref='order', lazy=True)
    status = db.Column(db.String(256), index=True)


class PurchasedMerch(db.Model):
    merch_id = db.Column(db.Integer, db.ForeignKey('sank_merch.id'), primary_key=True, nullable=False)
    variation_id = db.Column(db.Integer, db.ForeignKey('variation.id'))
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
