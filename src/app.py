from flask import Flask, request, jsonify

from .config import app_config
from .models import db, bcrypt
from .models import PlayerModel
from .models import GameModel

def create_app(env_name):
  """
  Create app
  """

  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  bcrypt.init_app(app)

  db.init_app(app)

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your first endpoint is workin'

  @app.route('/games', methods=['POST'])
  def add_game_request():
    organiser_id = request.json['organiser_id']
    opponent_id = request.json['opponent_id']
    game_date = request.json['game_date']
    game_time = request.json['game_time']

    new_game = GameModel(organiser_id, opponent_id, game_date, game_time)

    db.session.add(new_game)
    db.session.commit()

    return product_schema.jsonify(new_product)

  return app
