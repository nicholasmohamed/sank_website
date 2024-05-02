from flask import current_app
import datetime
from sqlalchemy.dialects.mysql import TIME
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
# TODO class for tags, will be handled


# database container for SankChewAir-E merchandise
class SankMerch(Base):
    __tablename__ = 'sank_merch'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), index=True)
    price = Column(Float, index=True)
    images = relationship('Image', backref='sank_merch', lazy=True)
    quantity = Column(Integer, index=True)
    isAvailable = Column(Boolean, index=True)
    sizes = relationship('Size', backref='sank_merch', lazy="joined")
    variations = relationship('Variation', backref='sank_merch', lazy=True)
    tags = Column(String(256), index=True)
    translations = relationship('SankMerchTranslations', backref='sank_merch', lazy="joined")

    def __repr__(self):
        return '<SankMerch {}>'.format(self.message)


class SankMerchTranslations(Base):
    __tablename__ = 'sank_merch_translations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String(256), index=True)
    description = Column(String(256), index=True)
    long_description = Column(String(512), index=True)
    manufacturing_description = Column(String(512), index=True)
    care_instructions = Column(String(512), index=True)
    merch_id = Column(Integer, ForeignKey('sank_merch.id'), nullable=False)


class Size(Base):
    __tablename__ = 'size'
    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String(256), index=True)
    size = Column(String(256), index=True)
    measurement = Column(String(256), index=True)
    merch_id = Column(Integer, ForeignKey('sank_merch.id'), nullable=False)


class Variation(Base):
    __tablename__ = 'variation'
    id = Column(Integer, primary_key=True)
    language = Column(String(256), index=True)
    name = Column(String(256), index=True)
    price = Column(Float, index=True)
    product_id = Column(Integer, ForeignKey('sank_merch.id'), index=True, nullable=False)
    color = Column(String(256), index=True)
    Materials = Column(String(256), index=True)


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, autoincrement=True)
    imageLink = Column(String(256), index=True)
    merch_id = Column(Integer, ForeignKey('sank_merch.id'), nullable=False)


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, index=True, default=datetime.datetime.now())
    purchased_merch = relationship('PurchasedMerch', backref='order', lazy=True)
    status = Column(String(256), index=True)


class PurchasedMerch(Base):
    __tablename__ = 'purchased_merch'
    merch_id = Column(Integer, ForeignKey('sank_merch.id'), primary_key=True, nullable=False)
    variation_id = Column(Integer, ForeignKey('variation.id'))
    size_id = Column(Integer, ForeignKey('size.id'))
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
