import datetime
from . import db # import db instance from models/__init__.py
from marshmallow import fields, Schema
from sqlalchemy import or_

class MessageModel(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    sender = db.relationship("PlayerModel", primaryjoin = "MessageModel.sender_id == PlayerModel.id", backref="sender")
    receiver = db.relationship("PlayerModel", primaryjoin = "MessageModel.receiver_id == PlayerModel.id", backref="receiver")

    def __init__(self, data):
        self.sender_id = data.get('sender_id')
        self.receiver_id = data.get('receiver_id')
        self.content = data.get('content')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
      db.session.add(self)
      db.session.commit()

    def update(self, data):
      for key, item in data.items():
        setattr(self, key, item)
      self.modified_at = datetime.datetime.utcnow()
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    @staticmethod
    def get_all_messages_with_user(current_user_id, other_user_id):
      return MessageModel.query.filter(or_(MessageModel.sender_id==current_user_id, MessageModel.receiver_id==current_user_id)).\
                                filter(or_(MessageModel.sender_id==other_user_id, MessageModel.receiver_id==other_user_id)).\
                                order_by(MessageModel.created_at.desc())

    def __repr__(self):
      return '<id {}>'.format(self.id)

class MessageSchema(Schema):
  """
  Message Schema
  """
  id = fields.Int(dump_only=True)
  sender_id = fields.Int(required=True)
  receiver_id = fields.Int(required=True)
  content = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
