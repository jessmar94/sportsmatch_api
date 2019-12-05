from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.MessageModel import MessageModel, MessageSchema
from ..models.PlayerModel import PlayerModel

message_api = Blueprint('message_api', __name__)
message_schema = MessageSchema()

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

@message_api.route('/<int:game_id>', methods=['GET'])
@Auth.auth_required
def get_all_messages(game_id):
    """
    Get all messages for game
    """
    message = MessageModel.get_all_game_messages(game_id).first()
    if not message:
        return custom_response({'message': 'No previous messages, start your conversation now', "player_postcode": PlayerModel.get_player_postcode(Auth.current_user_id())}, 200)
    messages = MessageModel.get_all_game_messages(game_id)
    data = message_schema.dump(messages, many=True)
    player = PlayerModel.get_player_postcode(Auth.current_user_id())
    data.append({
        'organiser': message.game.organiser.first_name,
        'opponent': message.game.opponent.first_name,
        'organiser_id': message.game.organiser_id,
        'opponent_id': message.game.opponent_id,
        "player_postcode": player['postcode']
    })
    print(data)
    return custom_response(data, 200)

@message_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Message
    """
    req_data = request.get_json()
    print(req_data)
    data = message_schema.load(req_data)
    message = MessageModel(data)
    message.save()
    data = message_schema.dump(message)
    return custom_response(data, 201)
