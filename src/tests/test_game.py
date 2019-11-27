import unittest
import os
import json
from ..models.PlayerModel import PlayerModel, PlayerSchema
from ..app import create_app, db
from ..shared.Authentication import Auth

class GamesTest(unittest.TestCase):
  """
  Results Test Case
  """
  def setUp(self):
    """
    Test Setup: runs before each test case method, creates the app and db tables
    """
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
      "email": "pam@spam.com",
      "password": "password",
      "gender": "F",
      "dob": "1991-01-01",
      "ability": "Advanced"
    }

    with self.app.app_context():
      db.create_all()
      player = PlayerModel(self.player_1)
      db.session.add(player)
      db.session.commit()
      db.session.refresh(player)
      player_1_id = player.id
      player = PlayerModel(self.player_2)
      player_2 = db.session.add(player)
      print(player_1_id)
      db.session.commit()

    self.game = {
      "organiser_id": 3,
      "opponent_id": 4,
      "confirmed": "false",
      "game_date": "2019-11-01",
      "game_time": "17:00:00"
    }

  def test_game_created(self):
    """ test game is created with valid credentials """
    auth = Auth
    token = auth.generate_token
    print('token')
    print(token)
    res = self.client().post('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': token}, data=json.dumps(self.game))
    json_data = json.loads(res.data)
    # self.assertTrue(json_data.get('opponent_id'))
    self.assertEqual(res.status_code, 201)
  
  def tearDown(self):
    """
    Runs at the end of the test case; drops the db
    """
    with self.app.app_context():
      db.session.remove()
      db.drop_all()

if __name__ == "__main__":
  unittest.main()