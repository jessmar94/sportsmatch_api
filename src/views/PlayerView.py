# request contains info from user including headers, body and other info
# json to serialize json output
from flask import request, json, Response, Blueprint, g
from ..models.PlayerModel import PlayerModel, PlayerSchema
# Auth used to generate user's token and to decode user's token
from ..shared.Authentication import Auth

player_api = Blueprint('player', __name__)
player_schema = PlayerSchema()

@player_api.route('/', methods=['POST'])
def create():
  """
  Create User Function
  """
  # request similar to http
  req_data = request.get_json()
  # load in format of playerschema
  data = player_schema.load(req_data)

  # if error:
  #   return custom_response(error, 400)
  
  # check if user already exist in the db
  player_in_db = PlayerModel.get_player_by_email(data.get('email'))
  if player_in_db:
    message = {'error': 'Player already exist, please supply another email address'}
    return custom_response(message, 400)
  
  player = PlayerModel(data)
  player.save()

  ser_data = player_schema.dump(player)

  token = Auth.generate_token(ser_data.get('id'))

  return custom_response({'jwt_token': token}, 201)
  
@player_api.route('/<int:player_id>', methods=['GET'])
@Auth.auth_required
def get_a_player(player_id):
  """
  Get a single player
  """
  player = PlayerModel.get_one_player(player_id)
  if not player:
    return custom_response({'error': 'player not found'}, 404)
  
  ser_player = player_schema.dump(player)
  return custom_response(ser_player, 200)

@player_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
  """
  Update me
  """
  req_data = request.get_json()
  data = player_schema.load(req_data, partial=True)
  # if error:
  #   return custom_response(error, 400)

  player = PlayerModel.get_one_player(g.player.get('id'))
  player.update(data)
  ser_player = player_schema.dump(player)
  return custom_response(ser_player, 200)

@player_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
  """
  Delete a player
  """
  player = PlayerModel.get_one_player(g.player.get('id'))
  player.delete()
  return custom_response({'message': 'deleted'}, 204)

@player_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
  """
  Get me
  """
  player = PlayerModel.get_one_player(g.player.get('id'))
  ser_player = player_schema.dump(player)
  return custom_response(ser_player, 200)

@player_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  players = PlayerModel.get_all_players()
  ser_players = player_schema.dump(players, many=True)
  return custom_response(ser_players, 200)

@player_api.route('/login', methods=['POST'])
def login():
  req_data = request.get_json()

  data = player_schema.load(req_data, partial=True)

  # if error:
  #   return custom_response(error, 400)
  
  if not data.get('email') or not data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 400)
  
  player = PlayerModel.get_player_by_email(data.get('email'))

  if not player:
    return custom_response({'error': 'invalid credentials'}, 400)
  
  if not player.check_hash(data.get('password')):
    return custom_response({'error': 'invalid credentials'}, 400)
  
  ser_data = player_schema.dump(player)
  
  token = Auth.generate_token(ser_data.get('id'))

  return custom_response({'jwt_token': token}, 200)

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )