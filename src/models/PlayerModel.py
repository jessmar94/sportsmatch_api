from marshmallow import fields, Schema
from sqlalchemy.orm import load_only
import datetime
from . import db # import db instance from models/__init__.py
from ..app import bcrypt
from .GameModel import GameSchema
from .ResultModel import ResultSchema
import pgeocode
# import from sqlalchemy import and_

class PlayerModel(db.Model): # PlayerModel class inherits from db.Model
  """
  Player Model
  """
  INITIAL_RANKS = {'Beginner': 50, 'Intermediate': 150, 'Advanced': 250}

  # name our table 'players'
  __tablename__ = 'players'

  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(60), nullable=False)
  last_name = db.Column(db.String(60), nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  postcode = db.Column(db.String(20), nullable=False)
  gender = db.Column(db.String(50), nullable=False)
  ability = db.Column(db.String(50), nullable=False)
  rank_points = db.Column(db.Integer, nullable=False)
  dob = db.Column(db.Date, nullable=False)
  profile_image = db.Column(db.LargeBinary, nullable=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  # class constructor to set class attributes
  def __init__(self, data):
    """
    Player Model
    """
    self.first_name = data.get('first_name')
    self.last_name = data.get('last_name')
    self.email = data.get('email')
    self.password = self.__generate_hash(data.get('password'))
    self.gender = data.get('gender')
    self.ability = data.get('ability')
    self.rank_points = self.set_rank_points(data.get('ability'))
    self.dob = data.get('dob')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()
    self.profile_image = data.get('profile_image')
    self.postcode = data.get('postcode')

  def set_rank_points(self, ability):
      return self.INITIAL_RANKS[ability]

  # def update_rank:

  def update_rank_points(self):
      setattr(self, 'rank_points', getattr(self, 'rank_points') + 5)
      self.modified_at = datetime.datetime.utcnow()
      db.session.commit()


  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
        if key == 'password':
            self.password = self.__generate_hash(value)
        setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
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
  def get_player_by_id(value):
    return PlayerModel.query.filter_by(id=value).first()

  @staticmethod
  def get_one_player(id):
    return PlayerModel.query.get(id)

  @staticmethod
  def get_opponent_info(id):
    player_schema = PlayerSchema()
    player = PlayerModel.query.with_entities(PlayerModel.first_name).filter_by(id=id).first()
    return player_schema.dump(player)

  @staticmethod
  def get_players_by_ability(value):
    user_schema = PlayerSchema()
    user = PlayerModel.query.filter_by(id=value).first()
    serialized_user = user_schema.dump(user)
    user_ability = serialized_user['ability']
    user_postcode = serialized_user['postcode']
    # players = PlayerModel.get_all_players()
    players = PlayerModel.query.filter(PlayerModel.ability==user_ability, PlayerModel.id != value)
    return players


  @staticmethod
  def get_players_within_distance(value):
      user_schema = PlayerSchema()
      user = PlayerModel.query.filter_by(id=value).first()
      serialized_user = user_schema.dump(user)
      user_ability = serialized_user['ability']
      user_postcode = serialized_user['postcode']
      players = PlayerModel.get_players_by_ability(value)
      filtered_array = []
      for player in players:
          results = PlayerModel.get_distance_between_postcodes(player.postcode, user_postcode, player.id)
          distances = int(round(results[0]))
          if distances <= 5:
              answer = PlayerModel.get_player_by_id(results[1])
              filtered_array.append(answer)
      return filtered_array

  @staticmethod
  def get_distance_between_postcodes(org_code, opp_code, opp_id):
     new_org_code = org_code[:-3].upper()
     new_opp_code = opp_code[:-3].upper()
     country = pgeocode.GeoDistance('gb')
     distance = [country.query_postal_code(new_org_code, new_opp_code), opp_id]
     return distance

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
    rank_points = fields.Int(required=False)
    gender = fields.Str(required=True)
    dob = fields.Date(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    games = fields.Nested(GameSchema, many=True)
    postcode = fields.Str(required=True)
