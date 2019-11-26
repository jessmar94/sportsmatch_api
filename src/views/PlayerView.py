from flask import request, json, Response, Blueprint
from ..models.PlayerModel import PlayerModel, PlayerSchema
from ..shared.Authentication import Auth

player_api = Blueprint('player', __name__)
player_schema = PlayerSchema()

@player_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create User Function
  """
  req_data = request.get_json()
  data = player_schema.load(req_data)

  # if error:
  #   return custom_response(error, 400) # 400 => server error

  # check if user already exist in the db
  player_in_db = PlayerModel.get_player_by_email(data.get('email'))
  if player_in_db:
    message = {'error': 'User already exist, please supply another email address'}
    return custom_response(message, 400)

  player = PlayerModel(data)
  player.save()

  ser_data = player_schema.dump(player)

  token = Auth.generate_token(ser_data.get('id'))

  return custom_response({'jwt_token': token}, 201)

@player_api.route('/<player_id>', methods=['GET'])
@Auth.auth_required
def get_player(player_id):
  """
  Get player by Id
  """
  player = PlayerModel.get_one_player(player_id)
  if not player:
    return custom_response({'error': 'player not found'}, 404)

  ser_player = player_schema.dump(player)
  return custom_response(ser_player, 200)

@player_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():

# @player_api.route('', methods=[''])
# @Auth.auth_required
# def update_player(player_id)


def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
