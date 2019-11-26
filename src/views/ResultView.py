from flask import request, json, Response, Blueprint
from ..models.ResultModel import ResultModel, ResultSchema
from ..models.GameModel import GameModel, GameSchema

result_api = Blueprint('results', __name__)
result_schema = ResultSchema()

@result_api.route('/', methods=['GET'])
def get_all():
    host = GameModel.get_game_by_org_id(1)
    guest = GameModel.get_game_by_opp_id(1)
    games = [*host, *guest]
    results = []
    for game in games:
        result = ResultModel.get_result_by_game(game.id)
        formatted_result = result_schema.dump(result, many=True)
        results.append(formatted_result)
    return custom_response(results, 200)

@result_api.route('/', methods=['POST'])
def create():
      """
      Create Result Function
      """
      # request similar to http
      req_data = request.get_json()
      # load in format of resultschema
      data = result_schema.load(req_data)

      result = ResultModel(data)
      result.save()
      return custom_response(data, 201)

@result_api.route('/<int:result_id>/edit', methods=['PATCH'])
def edit_result(result_id):
    """
    Edit a Result
    """
    req_data = request.get_json()
    result = ResultModel.get_one_result(result_id)
    if not result:
        return custom_response({'error': 'result not found'}, 404)
    data = result_schema.load(req_data, partial=True)
    result.update(data)
    data = result_schema.dump(result)
    return custom_response(data, 201)

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
