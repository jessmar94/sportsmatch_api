from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.GameModel import GameModel, GameSchema
from ..models.PlayerModel import PlayerModel, PlayerSchema
from ..models.ResultModel import ResultModel, ResultSchema

game_api = Blueprint('game_api', __name__)
game_schema = GameSchema()
player_schema = PlayerSchema()
result_schema = ResultSchema()

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
    Get All Games related to a user
    """
    user_id = Auth.current_user_id()
    games = GameModel.get_all_users_games(user_id)
    data = game_schema.dump(games, many=True)
    organiser = []
    challenger = []
    for game in data:
      if game['organiser_id'] == user_id:
        organiser.append({**game, **PlayerModel.get_opponent_info(game['opponent_id'])})
      elif game['opponent_id'] == user_id:
        challenger.append({**game, **PlayerModel.get_opponent_info(game['organiser_id'])})
    results ={'organiser_games': organiser, 'challenger_games': challenger}
    return custom_response(results, 200)

@game_api.route('/opponent', methods=['GET'])
@Auth.auth_required
def get_all_opponent_games():
    """
    Get Past Confirmed Games related to an opponent
    """
    current_user_id = Auth.current_user_id()
    guest = GameModel.get_game_by_opp_id(current_user_id)
    games = [*guest]
    results = []
    game_results = []
    for game in games:
        result = ResultModel.get_all_results(game.id)
        game = GameModel.get_games_by_id(game.id)
        formatted_result = result_schema.dump(result, many=True)
        formatted_game_info = game_schema.dump(game, many=True)
        organiser = PlayerModel.get_opponent_info(formatted_game_info[0]['organiser_id'])

        if len(formatted_result) == 0:
            final_results = {**formatted_game_info[0], **organiser}
            game_results.append(final_results)
        elif len(formatted_result) != 0:
            final_results = {**formatted_result[0], **formatted_game_info[0], **organiser}
            game_results.append(final_results)
    return custom_response(game_results, 200)

@game_api.route('/organiser', methods=['GET'])
@Auth.auth_required
def get_all_organiser_games():
    """
    Get Past Confirmed Games related to an opponent
    """
    current_user_id = Auth.current_user_id()
    host = GameModel.get_game_by_org_id(current_user_id)
    games = [*host]
    results = []
    game_results = []
    for game in games:
        result = ResultModel.get_all_results(game.id)
        game = GameModel.get_games_by_id(game.id)
        formatted_result = result_schema.dump(result, many=True)
        formatted_game_info = game_schema.dump(game, many=True)
        opponent = PlayerModel.get_opponent_info(formatted_game_info[0]['opponent_id'])

        if len(formatted_result) == 0:
            final_results = {**formatted_game_info[0], **opponent}
            game_results.append(final_results)
        elif len(formatted_result) != 0:
            final_results = {**formatted_result[0], **formatted_game_info[0], **opponent}
            game_results.append(final_results)

    return custom_response(game_results, 200)

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


# @game_api.route('/<int:game_id>', methods=['DELETE'])
# @Auth.auth_required
# def delete_game(game_id):
#     user_id = Auth.current_user_id()
#     game = GameModel.get_one_game(game_id)
#     data = game_schema.dump(game)
#     if not game:
#         return custom_response({'error': 'game not found'}, 404)
#     if data.get('organiser_id') == user_id:
#         return custom_response({'error': 'permission denied'}, 400)
#     game.delete()
#     return custom_response({'message': 'deleted'}, 204)
