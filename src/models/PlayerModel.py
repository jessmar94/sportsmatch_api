from marshmallow import fields, Schema
import datetime
from . import db # import db instance from models/__init__.py
from ..app import bcrypt
from .GameModel import GameSchema
from .ResultModel import ResultSchema

class PlayerModel(db.Model): # PlayerModel class inherits from db.Model
  """
  Player Model
  """

  # table name
  __tablename__ = 'players' # name our table players

  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(60), nullable=False)
  last_name = db.Column(db.String(60), nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  gender = db.Column(db.String(50), nullable=False)
  ability = db.Column(db.String(50), nullable=False)
  dob = db.Column(db.Date, nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  # organiser = db.relationship("GameModel",  backref="playerModel", lazy=True)
  # opponent = db.relationship("GameModel",  backref="playerModel", lazy=True)
  # winner = db.relationship("ResultModel",  backref="playerModel", lazy=True)
  # loser = db.relationship("ResultModel", backref="playerModel", lazy=True)

  # class constructor
  def __init__(self, data): # class constructor used to set the class attributes
    """
    Class constructor
    """
    self.first_name = data.get('first_name')
    self.last_name = data.get('last_name')
    self.email = data.get('email')
    self.password = self.__generate_hash(data.get('password'))
    self.gender = data.get('gender')
    self.ability = data.get('ability')
    self.dob = data.get('dob')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  def save(self): # use to save players to our db
    db.session.add(self)
    db.session.commit()

  def update(self, data): # use to update a player's record on the db
    for key, item in data.items():
        if key == 'password':
            self.password = self.__generate_hash(value)
        setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self): # use to delete record from the db
    db.session.delete(self)
    db.session.commit()

  def __generate_hash(self, password):
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

  def check_hash(self, password):
    return bcrypt.check_password_hash(self.password, password)

  @staticmethod
  def get_all_players():
    return PlayerModel.query.all()

  @staticmethod
  def get_player_by_email(value):
    return PlayerModel.query.filter_by(email=value).first()

  @staticmethod
  def get_one_player(id):
    return PlayerModel.query.get(id)


  def __repr__(self): # returns a printable representation of the PlayerModel object (returning the id only)
    return '<id {}>'.format(self.id)

class PlayerSchema(Schema):
  """
  Player Schema
  """
  id = fields.Int(dump_only=True)
  first_name = fields.Str(required=True)
  last_name = fields.Str(required=True)
  email = fields.Email(required=True)
  password = fields.Str(required=True)
  ability = fields.Str(required=True)
  gender = fields.Str(required=True)
  dob = fields.Date(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  games = fields.Nested(GameSchema, many=True)
