from flask_cors import CORS
from flask import Flask, render_template
from .config import app_config
from .models import db, bcrypt
from .models import PlayerModel
from .models import GameModel
from .models import ResultModel
from .views.ResultView import result_api as result_blueprint
from .views.PlayerView import player_api as player_blueprint

from .views.GameView import game_api as game_blueprint # add this line

def create_app(env_name):
  """
  Create app
  """

  # app initiliazation
  app = Flask(__name__)

  cors = CORS(app)

  app.config.from_object(app_config[env_name])
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['CORS_HEADERS'] = 'Content-Type'

  bcrypt.init_app(app)

  db.init_app(app)


  app.register_blueprint(game_blueprint, url_prefix='/api/v1/games')

  app.register_blueprint(result_blueprint, url_prefix='/api/v1/results')

  app.register_blueprint(player_blueprint, url_prefix='/api/v1/players')

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return "Initial root route"

  return app
