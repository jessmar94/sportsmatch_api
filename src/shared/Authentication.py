from flask_jwt import jwt, current_identity
import os
import datetime
from flask import json, Response, request, g
from ..models.PlayerModel import PlayerModel
from functools import wraps

class Auth():
  """
  Auth Class
  """
  @staticmethod
  def generate_token(player_id):
    """
    Generate Token Method
    """
    try:
      payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': player_id
      }
      return jwt.encode(
        payload,
        os.getenv('JWT_SECRET_KEY'),
        'HS256'
      ).decode("utf-8")
    except Exception as e:
      return Response(
        mimetype="application/json",
        response=json.dumps({'error': 'error in generating player token'}),
        status=400
      )

  @staticmethod
  def decode_token(token):
    """
    Decode token method
    """
    re = {'data': {}, 'error': {}}
    try:
      payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
      re['data'] = {'player_id': payload['sub']}
      return re
    except jwt.ExpiredSignatureError as e1:
      re['error'] = {'message': 'token expired, please login again'}
      return re
    except jwt.InvalidTokenError:
      re['error'] = {'message': 'Invalid token, please try again with a new token'}
      return re

  @staticmethod
  def current_user_id():
    token = request.headers.get('api-token')
    data = Auth.decode_token(token)
    return data['data']['player_id']

  @staticmethod
  def auth_required(func):
    """
    Auth decorator
    """
    @wraps(func)
    def decorated_auth(*args, **kwargs):
      if 'api-token' not in request.headers:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
          status=400
        )
      token = request.headers.get('api-token')
      data = Auth.decode_token(token)
      if data['error']:
        return Response(
          mimetype="application/json",
          response=json.dumps(data['error']),
          status=400
        )

      player_id = data['data']['player_id']

      check_player = PlayerModel.get_one_player(player_id)
      if not check_player:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'player does not exist, invalid token'}),
          status=400
        )
        # if token is valid, save the payload data to g (g is a global variable in flask)
      g.player = {'id': player_id}
      return func(*args, **kwargs)
    return decorated_auth
