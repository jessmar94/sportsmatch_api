import unittest
import os
import json
from ..app import create_app, db
from ..models.PlayerModel import PlayerModel, PlayerSchema
from ..models.GameModel import GameModel, GameSchema
from ..models.ResultModel import ResultModel, ResultSchema

class ResultsTest(unittest.TestCase):
  """
  Results Test Case
  """
  def setUp(self):
    self.app = create_app("test")
    self.client = self.app.test_client
    self.player_1 = {
      "first_name": "Dom",
      "last_name": "T",
      "email": "dom@test.com",
      "password": "password",
      "gender": "M",
      "dob": "1990-01-01",
      "ability": "Beginner"
    }
    self.player_2 = {
      "first_name": "Pam",
      "last_name": "M",
      "email": "pam@test.com",
      "password": "password",
      "gender": "F",
      "dob": "1990-01-01",
      "ability": "Beginner"
    }
    self.game_1 = {
      "organiser_id": 1,
      "opponent_id": 2,
      "confirmed": "False",
      "game_date": "2019-01-01",
      "game_time": "15:00:00"
    }
    self.result_1 = {
      "game_id": 1,
      "winner_id": 2,
      "loser_id": 1,
      "confirmed": "False"
    }

    with self.app.app_context():
      db.create_all()
      player1 = PlayerModel(self.player_1)
      player2 = PlayerModel(self.player_2)
      db.session.add(player1)
      db.session.add(player2)

      game1 = GameModel(self.game_1)
      db.session.add(game1)

      db.session.commit()

  def test_create_a_result(self):
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
    api_token = json.loads(res.data).get('jwt_token')
    print(api_token)
    res = self.client().post('api/v1/results/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.result_1))
    json_data = json.loads(res.data)
    print(json_data)
    self.assertEqual(res.status_code, 201)

  # def test_create_

  def tearDown(self):
    """
    Runs at the end of the test case; drops the db
    """
    with self.app.app_context():
      db.session.remove()
      db.drop_all()

if __name__ == "__main__":
  unittest.main()