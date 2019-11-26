from flask import Flask

from .config import app_config
from .models import db, bcrypt
from .models import PlayerModel
from .models import GameModel
from .models import ResultModel
from .views.ResultView import result_api as result_blueprint
from .views.PlayerView import player_api as player_blueprint

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

  app.register_blueprint(result_blueprint, url_prefix='/api/v1/players/1/results')
  app.register_blueprint(player_blueprint, url_prefix='/api/v1/players')


  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your first endpoint is working'

  return app
