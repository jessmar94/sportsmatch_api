import flask from Flask, request, jsonify
import flask-sqlalchemy from SQLalchemy
import flask-migrate from Migrate
import marshmallow from Marshmallow
import datetime
from . import db # import db instance from models/__init__.py
from ..app import bcrypt

class GamesModel(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    booking_date = db.Column(db.DateTime)

    def __init__(self, data):
        self.requester_id = data.get('requester_id')
        self.receiver_id = data.get('receiver_id')
        self.confirmed = data.get('confirmed')
        self.booking_date = datetime.datetime.utcnow() ##CHANGE

class ProductSchema(ma.Schema):
    class Meta:
    fields = ('id', 'name', 'description', 'price', 'qty')

#Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
