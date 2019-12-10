from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.MessageModel import MessageModel, MessageSchema
from ..models.PlayerModel import PlayerModel

message_api = Blueprint('message_api', __name__)
message_schema = MessageSchema()

def custom_response(res, status_code):
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

@message_api.route('/<int:other_user_id>', methods=['GET'])
@Auth.auth_required
def get_all_messages(other_user_id):
    message = MessageModel.get_all_messages_with_user(Auth.current_user_id(), other_user_id).first()
    if not message:
        return custom_response({'message': 'No previous messages, start your conversation now', "player_postcode": PlayerModel.get_player_postcode(Auth.current_user_id())}, 200)
    messages = MessageModel.get_all_messages_with_user(Auth.current_user_id(), other_user_id)
    data = message_schema.dump(messages, many=True)
    player = PlayerModel.get_player_postcode(Auth.current_user_id())
    data.append({
        'sender': message.sender.first_name,
        'receiver': message.receiver.first_name,
        "player_postcode": player['postcode']
    })
    return custom_response(data, 200)

@message_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    print(req_data)
    data = message_schema.load(req_data)
    content = data.get('content')
    if not content:
        message = {'error': 'Message cannot be empty'}
        return custom_response(message, 400)
    message = MessageModel(data)
    message.save()
    data = message_schema.dump(message)
    return custom_response(data, 201)
