from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.GameModel import GameModel, GameSchema

game_api = Blueprint('game_api', __name__)
game_schema = GameSchema()

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

@game_api.route('/<int:game_id>', methods=['GET'])
@Auth.auth_required
def get_one(game_id):
  """
  Get A Game
  """
  game = GameModel.get_one_game(game_id)
  if not game:
    return custom_response({'error': 'game not found'}, 404)
  data = game_schema.dump(game)
  return custom_response(data, 200)

@game_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    """
    Get All Games
    """
    user_id = Auth.current_user_id()
    game = GameModel.get_all_games(user_id)
    data = game_schema.dump(game, many=True)
    return custom_response(data, 200)

@game_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Game Function
  """
  req_data = request.get_json()
  data = game_schema.load(req_data)
  game = GameModel(data)
  game.save()
  data = game_schema.dump(game)
  return custom_response(data, 201)

@game_api.route('/<int:game_id>', methods=['PATCH'])
@Auth.auth_required
def confirm_game(game_id):
    """
    Confirm a Game
    """
    user_id = Auth.current_user_id()
    req_data = request.get_json()
    game = GameModel.get_one_game(game_id)
    data = game_schema.dump(game)
    if not game:
        return custom_response({'error': 'game not found'}, 404)
    if data.get('opponent_id') != user_id:
        return custom_response({'error': 'permission denied'}, 400)
    data = game_schema.load(req_data, partial=True)
    game.update(data)
    data = game_schema.dump(game)
    return custom_response(data, 201)

@game_api.route('/<int:game_id>/edit', methods=['PATCH'])
@Auth.auth_required
def edit_game(game_id):
    """
    Edit a Game
    """
    user_id = Auth.current_user_id()
    req_data = request.get_json()
    game = GameModel.get_one_game(game_id)
    data = game_schema.dump(game)
    if not game:
        return custom_response({'error': 'game not found'}, 404)
    if data.get('organiser_id') == user_id\
        or data.get('opponent_id') == user_id:
            data = game_schema.load(req_data, partial=True)
            game.update(data)
            data = game_schema.dump(game)
            return custom_response(data, 201)
    else:
        return custom_response({'error': 'permission denied'}, 400)


@game_api.route('/<int:game_id>', methods=['DELETE'])
@Auth.auth_required
def delete_game(game_id):
    user_id = Auth.current_user_id()
    game = GameModel.get_one_game(game_id)
    data = game_schema.dump(game)
    if not game:
        return custom_response({'error': 'game not found'}, 404)
    if data.get('organiser_id') != user_id:
        return custom_response({'error': 'permission denied'}, 400)
    game.delete()
    return custom_response({'message': 'deleted'}, 204)
