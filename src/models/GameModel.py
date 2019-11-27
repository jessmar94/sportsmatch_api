import datetime
from . import db # import db instance from models/__init__.py
from marshmallow import fields, Schema
from .ResultModel import ResultSchema
from sqlalchemy import or_

class GameModel(db.Model): # GameModel class inherits from db.Model
  """
  Game Model
  """

  # table name
  __tablename__ = 'games' # name our table Games

  id = db.Column(db.Integer, primary_key=True)
  organiser_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
  opponent_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
  confirmed = db.Column(db.Boolean, default=False, nullable=False)
  game_date = db.Column(db.Date, nullable=False)
  game_time = db.Column(db.Time, nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  organiser = db.relationship("PlayerModel", foreign_keys=[organiser_id])
  opponent = db.relationship("PlayerModel", foreign_keys=[opponent_id])
  game = db.relationship("ResultModel", backref="gameModel", lazy=True)

  # class constructor
  def __init__(self, data): # class constructor used to set the class attributes
    """
    Class constructor
    """
    self.organiser_id = data.get('organiser_id')
    self.opponent_id = data.get('opponent_id')
    self.game_date = data.get('game_date')
    self.game_time = data.get('game_time')
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
  def get_all_games(id):
    return GameModel.query.filter(or_(GameModel.organiser_id==id, GameModel.opponent_id==id))

  @staticmethod
  def get_one_game(id):
    return GameModel.query.get(id)

  @staticmethod
  def get_game_by_org_id(user_id):
    return GameModel.query.filter_by(organiser_id=user_id).filter(GameModel.confirmed.is_(True), GameModel.game_date <= datetime.datetime.utcnow())

  @staticmethod
  def get_game_by_opp_id(user_id):
    return GameModel.query.filter_by(opponent_id=user_id).filter(GameModel.confirmed.is_(True), GameModel.game_date <= datetime.datetime.utcnow())

  def __repr__(self):
    return '<id {}>'.format(self.id)

class GameSchema(Schema):
  """
  Game Schema
  """
  id = fields.Int(dump_only=True)
  organiser_id = fields.Int(required=True)
  opponent_id = fields.Int(required=True)
  game_date = fields.Date(required=True)
  game_time = fields.Time(required=True)
  confirmed = fields.Boolean(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
