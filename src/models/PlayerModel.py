from marshmallow import fields, Schema
from sqlalchemy.orm import load_only
import datetime
from . import db # import db instance from models/__init__.py
from ..app import bcrypt
from .GameModel import GameSchema
from .ResultModel import ResultSchema
from .MessageModel import MessageSchema
import pgeocode
# import from sqlalchemy import and_

class PlayerModel(db.Model): # PlayerModel class inherits from db.Model
  """
  Player Model
  """
  RANKS = {'Beginner': 100, 'Intermediate': 200, 'Advanced': 300}
  # ABILITIES = {range(0,100): 'Beginner', range(101,200):'Intermediate', range(201,..): 'Advanced'}
  # abiltiy = ['Beginner', 'Intermediate', 'Advanced']

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
      return self.RANKS[ability]/2

  # def update_rank:

  def update_winner_rank_points(self):
      new_points = getattr(self, 'rank_points') + 5
      current_ability = getattr(self, 'ability')

      if new_points > self.RANKS[current_ability]:
        if current_ability == 'Beginner':
         setattr(self, 'ability', 'Intermediate')
        elif current_ability == 'Intermediate':
            setattr(self, 'ability', 'Advanced')

      setattr(self, 'rank_points', new_points)
      self.modified_at = datetime.datetime.utcnow()
      db.session.commit()

  def update_loser_rank_points(self):
      new_points = getattr(self, 'rank_points') - 5
      current_ability = getattr(self, 'ability')

      if new_points <= self.RANKS[current_ability]:
        if current_ability == 'Advanced':
         setattr(self, 'ability', 'Intermediate')
        elif current_ability == 'Intermediate':
            setattr(self, 'ability', 'Beginner')

      setattr(self, 'rank_points', new_points)
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
  def get_player_profile_image(id):
    return PlayerModel.query.with_entities(PlayerModel.profile_image).filter_by(id=id).first()

  @staticmethod
  def get_one_player(id):
    return PlayerModel.query.with_entities(
        PlayerModel.first_name,
        PlayerModel.last_name,
        PlayerModel.email,
        PlayerModel.dob,
        PlayerModel.ability,
        PlayerModel.gender
    ).filter_by(id=id).first()

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
              answer = PlayerModel.get_one_player(results[1])
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

class BytesField(fields.Field):
    """
    Creating custom field for scheme that serializes base64 to LargeBinary
    and desrializes LargeBinary to base64
    """

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return ""
        binary_string = bin(int.from_bytes(value.encode(), 'big'))
        binary = bytes(binary_string, 'utf-8')
        return binary

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        binary_string = int(value,2)
        base64_string = binary_string.to_bytes((binary_string.bit_length() + 7) // 8, 'big').decode()
        return base64_string

class PlayerSchema(Schema):
    """
    Player Schema
    """

    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    ability = fields.Str(required=True)
    rank_points = fields.Int(required=False)
    gender = fields.Str(required=True)
    dob = fields.Date(required=True)
    profile_image = BytesField(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    games = fields.Nested(GameSchema, many=True)
    postcode = fields.Str(required=True)
