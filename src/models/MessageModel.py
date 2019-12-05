import datetime
from . import db  # import db instance from models/__init__.py
from marshmallow import fields, Schema


class MessageModel(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    organiser_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    opponent_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    host = db.relationship("PlayerModel", primaryjoin = "MessageModel.organiser_id == PlayerModel.id", backref="host")
    client = db.relationship("PlayerModel", primaryjoin = "MessageModel.opponent_id == PlayerModel.id", backref="client")
    sender = db.relationship("PlayerModel", primaryjoin = "MessageModel.sender_id == PlayerModel.id", backref="sender")
    game = db.relationship("GameModel", back_populates="message")

    def __init__(self, data):
        self.game_id = data.get('game_id')
        self.sender_id = data.get('sender_id')
        self.organiser_id = data.get('organiser_id')
        self.opponent_id = data.get('opponent_id')
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
    def get_all_game_messages(game_id):
      return MessageModel.query.filter_by(game_id=game_id)

    def __repr__(self):
      return '<id {}>'.format(self.id)


class MessageSchema(Schema):
  """
  Message Schema
  """
  id = fields.Int(dump_only=True)
  game_id = fields.Int(required=True)
  sender_id = fields.Int(required=True)
  organiser_id = fields.Int(required=True)
  opponent_id = fields.Int(required=True)
  content = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
