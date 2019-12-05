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
      "ability": "Beginner",
      "postcode": "N169NP"
    }

    self.player_2 = {
      "first_name": "Pam",
      "last_name": "M",
      "email": "pam@spam.com",
      "password": "password",
      "gender": "F",
      "dob": "1991-01-01",
      "ability": "Advanced",
      "postcode": "N169NP"
    }

    self.player_3 = {
      "first_name": "Jess",
      "last_name": "M",
      "email": "jess@spam.com",
      "password": "password",
      "gender": "F",
      "dob": "1991-01-01",
      "ability": "Advanced",
      "postcode": "N169NP"
    }

    with self.app.app_context():
      db.create_all()
      player = PlayerModel(self.player_1)
      db.session.add(player)
      db.session.commit()
      db.session.refresh(player)
      player_1_id = player.id
      player2 = PlayerModel(self.player_2)
      db.session.add(player2)
      db.session.commit()
      db.session.refresh(player2)
      player_2_id = player2.id

    self.game = {
      "organiser_id": player_1_id,
      "opponent_id": player_2_id,
      "status": "pending",
      "game_date": "2019-11-01",
      "game_time": "17:00:00"
    }

    self.game_2 = {
      "organiser_id": player_2_id,
      "opponent_id": player_1_id,
      "status": "pending",
      "game_date": "2019-11-01",
      "game_time": "11:00:00"
    }

  def test_game_created(self):
    """ test game is created with valid credentials """
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().post('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.game))
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('organiser_id'), 1)
    self.assertEqual(res.status_code, 201)

  def test_return_one_game(self):
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().post('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.game))
    json_data = json.loads(res.data)
    res = self.client().get('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    organiser_id = json_data.get('organiser_games')[0].get('organiser_id')
    self.assertEqual(organiser_id, 1)
    self.assertEqual(res.status_code, 200)

  def test_return_all_games(self):
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().post('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.game))
    json_data = json.loads(res.data)
    res = self.client().post('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.game_2))
    json_data = json.loads(res.data)
    res = self.client().get('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)

    organiser_id = json_data.get('organiser_games')[0].get('organiser_id')
    opponent_id = json_data.get('challenger_games')[0].get('opponent_id')
    self.assertEqual(organiser_id, 1)
    self.assertEqual(opponent_id, 1)
    self.assertEqual(res.status_code, 200)

  def test_edit_game(self):
    updated_game = {
        "game_time": "12:00:00"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().post('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.game))
    json_data = json.loads(res.data)
    res = self.client().get('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    res = self.client().patch('api/v1/games/1/edit', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_game))
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('game_date'), "2019-11-01")
    self.assertEqual(json_data.get('game_time'), '12:00:00')
    self.assertEqual(res.status_code, 201)

  def test_error_when_edit_game_does_not_exist(self):
    updated_game = {
        "game_time": "12:00:00"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().post('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.game))
    json_data = json.loads(res.data)
    res = self.client().get('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    res = self.client().patch('api/v1/games/5/edit', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_game))
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('error'), 'game not found')
    self.assertEqual(res.status_code, 404)

  # def test_game_deleted(self):
  #   """ test game is deleted with valid credentials """
  #   res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
  #   api_token = json.loads(res.data).get('jwt_token')
  #   res = self.client().post('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.game))
  #   json_data = json.loads(res.data)
  #   res = self.client().get('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token})
  #   json_data = json.loads(res.data)
  #   res = self.client().delete('api/v1/games/1', headers={'Content-Type': 'application/json', 'api-token': api_token})
  #   self.assertEqual(res.status_code, 204)

  # def test_error_when_delete_game_that_does_not_exist(self):
  #   """ test game is deleted with valid credentials """
  #   res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
  #   api_token = json.loads(res.data).get('jwt_token')
  #   res = self.client().post('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.game))
  #   json_data = json.loads(res.data)
  #   res = self.client().get('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token})
  #   json_data = json.loads(res.data)
  #   res = self.client().delete('api/v1/games/4', headers={'Content-Type': 'application/json', 'api-token': api_token})
  #   json_data = json.loads(res.data)
  #   self.assertEqual(json_data.get('error'), 'game not found')
  #   self.assertEqual(res.status_code, 404)

  # def test_error_when_user_is_not_organiser(self):
  #   """ test game is deleted with valid credentials """
  #   res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_2))
  #   api_token = json.loads(res.data).get('jwt_token')
  #   res = self.client().post('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.game))
  #   json_data = json.loads(res.data)
  #   res = self.client().get('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token})
  #   json_data = json.loads(res.data)
  #   res = self.client().delete('api/v1/games/1', headers={'Content-Type': 'application/json', 'api-token': api_token})
  #   json_data = json.loads(res.data)
  #   self.assertEqual(json_data.get('error'), 'permission denied')
  #   self.assertEqual(res.status_code, 400)

  def tearDown(self):
    """
    Runs at the end of the test case; drops the db
    """
    with self.app.app_context():
      db.session.remove()
      db.drop_all()

if __name__ == "__main__":
  unittest.main()
