from flask import g, request, json, Response, Blueprint
from ..models.ResultModel import ResultModel, ResultSchema
from ..models.GameModel import GameModel, GameSchema
from ..shared.Authentication import Auth

result_api = Blueprint('results', __name__)
result_schema = ResultSchema()

@result_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    """
    Logged in player can view all results where they are the organiser or opponent
    """
    current_user_id = Auth.current_user_id()
    host = GameModel.get_game_by_org_id(current_user_id)
    guest = GameModel.get_game_by_opp_id(current_user_id)
    games = [*host, *guest]
    results = []
    for game in games:
        result = ResultModel.get_all_results(game.id)
        formatted_result = result_schema.dump(result, many=True)
        results.append(formatted_result)
    return custom_response(results, 200)

@result_api.route('/<int:game_id>/new', methods=['POST'])
@Auth.auth_required
def create(game_id):
      """
      Create Result Function
      """
      current_user_id = Auth.current_user_id()
      req_data = request.get_json()
      data = result_schema.load(req_data)
      result = ResultModel.get_result_by_game(game_id)
      if result:
          message = {'error': 'Result already provided'}
          return custom_response(message, 400)
      game = GameModel.get_one_game(game_id)
      if game.confirmed == False:
          message = {'error': 'Game needs to be confirmed to add a result'}
          return custom_response(message, 400)
      if game.organiser_id == current_user_id:
          result = ResultModel(data)
          result.save()
          return custom_response(data, 201)
      message = {'error': 'You can only add a result if you are the organiser.'}
      return custom_response(message, 404)

@result_api.route('/<int:result_id>/edit', methods=['PATCH'])
@Auth.auth_required
def edit_result(result_id):
    """
    Edit a Result
    """
    current_user_id = Auth.current_user_id()
    req_data = request.get_json()
    result = ResultModel.get_one_result(result_id)

    if not result:
        return custom_response({'error': 'result not found'}, 404)

    game = GameModel.get_one_game(result.game_id)

    if game.organiser_id == current_user_id:
        data = result_schema.load(req_data, partial=True)
        result.update(data)
        data = result_schema.dump(result)
        return custom_response(data, 201)
    else:
        return custom_response({'error': 'only organiser can edit the result'}, 404)

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
