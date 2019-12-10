from flask import g, request, json, Response, Blueprint
from ..models.PlayerModel import PlayerModel
from ..models.ResultModel import ResultModel, ResultSchema
from ..models.GameModel import GameModel, GameSchema
from ..shared.Authentication import Auth

result_api = Blueprint('results', __name__)
result_schema = ResultSchema()
game_schema = GameSchema()

# @result_api.route('/<int:result_id>', methods=['GET'])
# @Auth.auth_required
# def show_one_result(result_id):
#     current_user_id = Auth.current_user_id()
#
#     result = ResultModel.get_one_result(result_id)
#     if result.winner_id == current_user_id or result.loser_id == current_user_id:
#             data = result_schema.dump(result)
#             return custom_response(data, 200)
#
#     message = {'error': 'You must have played in this game to view the result.'}
#     return custom_response(message, 404)

@result_api.route('/<int:game_id>/new', methods=['POST'])
@Auth.auth_required
def create(game_id):
      current_user_id = Auth.current_user_id()
      req_data = request.get_json()
      winner = PlayerModel.get_one_player(req_data['winner_id'])
      loser = PlayerModel.get_one_player(req_data['loser_id'])
      data = result_schema.load(req_data)
      result = ResultModel.get_result_by_game(game_id)
      if result:
          message = {'error': 'Result already provided'}
          return custom_response(message, 400)
      game = GameModel.get_one_game(game_id)
      if game.status != "confirmed":
          message = {'error': 'Game needs to be confirmed to add a result'}
          return custom_response(message, 400)
      if game.organiser_id == current_user_id:
          result = ResultModel(data)
          winner.update_winner_rank_points()
          loser.update_loser_rank_points()
          result.save()
          return custom_response(data, 201)
      message = {'error': 'You can only add a result if you are the organiser.'}
      return custom_response(message, 400)

def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
