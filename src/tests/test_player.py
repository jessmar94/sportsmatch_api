import unittest
import os
import json
from ..app import create_app, db
from ..models.PlayerModel import PlayerModel, PlayerSchema

class PlayersTest(unittest.TestCase):
  """
  Players Test Case
  """
  def setUp(self):
    """
    Test Setup: runs before each test case method, creates the app and db tables
    """
    self.app = create_app("test")
    self.client = self.app.test_client
    self.player = {
      "first_name": "Dom",
      "last_name": "T",
      "email": "dom@test.com",
      "password": "password",
      "gender": "Male",
      "dob": "1990-01-01",
      "ability": "Beginner",
      "postcode": "N65HQ",
      "rank_points": 50
    }
    self.player2 = {
      "first_name": "Bob",
      "last_name": "T",
      "email": "bob@test.com",
      "password": "password",
      "gender": "Male",
      "dob": "1990-01-01",
      "ability": "Beginner",
      "postcode": "N65HQ",
      "rank_points": 50
    }
    with self.app.app_context():
        db.create_all()
        player2 = PlayerModel(self.player2)
        db.session.add(player2)
        db.session.commit()
        db.session.refresh(player2)
        player2_id = player2.id

    # with self.app.app_context():
    #   db.create_all()

  def test_player_created(self):
    """ test player is created with valid credentials """
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    json_data = json.loads(res.data)
    self.assertTrue(json_data.get('jwt_token'))
    self.assertEqual(res.status_code, 201)

  def test_error_when_existing_email_used_to_create_account(self):
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    self.assertEqual(res.status_code, 201)
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error'), 'Player already exist, please supply another email address')

  def test_get_user_image(self):
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player2))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().get('api/v1/players/1/image', headers={'Content-Type': 'application/json', 'api-token': api_token} )
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)

  def test_player_login(self):
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player2))
    json_data = json.loads(res.data)
    self.assertTrue(json_data.get('jwt_token'))
    self.assertEqual(res.status_code, 200)

  def test_error_when_player_login_with_invalid_password(self):
    invalid_password_player = {
      "email": "bob@test.com",
      "password": "dgfdgdfg!"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(invalid_password_player))
    json_data = json.loads(res.data)
    self.assertFalse(json_data.get('jwt_token'))
    self.assertEqual(json_data.get('error'), 'invalid password')
    self.assertEqual(res.status_code, 400)

  def test_error_when_player_login_with_invalid_email(self):
    invalid_email_player = {
      "email": "bob@te.com",
      "password": "password"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(invalid_email_player))
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('error'), 'invalid credentials')
    self.assertFalse(json_data.get('jwt_token'))
    self.assertEqual(res.status_code, 400)

  def test_error_user_logs_in_without_email(self):
    incomplete_player = {
      "password": "password"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(incomplete_player))
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('error'), 'you need email and password to sign in')
    self.assertFalse(json_data.get('jwt_token'))
    self.assertEqual(res.status_code, 400)

  def test_user1_can_see_user2(self):
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.player))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().get('api/v1/players/1', headers={'Content-Type': 'application/json', 'api-token': api_token} )
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('first_name'), "Bob")
    self.assertEqual(res.status_code, 200)

  def test_user1_cannot_see_nonexistant_user(self):
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.player))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().get('api/v1/players/10', headers={'Content-Type': 'application/json'} )
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)

  def test_player_can_view_their_own_profile(self):
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player2))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().get('api/v1/players/my_profile', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('email'), 'bob@test.com')
    self.assertEqual(json_data.get('first_name'), 'Bob')

  def test_get_all_filtered_players(self):
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player2))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().get('api/v1/players/', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)

  def test_player_gets_points_if_wins(self):
    updated_game = {
      "status": "confirmed"
    }
    game = {
        "organiser_id": 1,
        "opponent_id": 2,
        "status": "pending",
        "game_date": "2019-10-22",
        "game_time": "15:00"
    }
    result = {
        "game_id": 1,
        "winner_id": 1,
        "loser_id": 2,
        "result_confirmed": True
    }
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player2))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().post('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(game))
    res = self.client().patch('api/v1/games/1/edit', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_game))
    res = self.client().post("api/v1/results/1/new", headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(result))
    res = self.client().get("api/v1/players/1", headers={'Content-Type': 'application/json', 'api-token': api_token} )
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('rank_points'), 55)

  def test_player_loses_5_points_if_lost(self):
    updated_game = {
      "status": "confirmed"
    }
    game = {
        "organiser_id": 1,
        "opponent_id": 2,
        "status": "pending",
        "game_date": "2019-10-22",
        "game_time": "15:00"
    }
    result = {
        "game_id": 1,
        "winner_id": 2,
        "loser_id": 1,
        "result_confirmed": True
    }
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player2))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().post('api/v1/games/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(game))
    res = self.client().patch('api/v1/games/1/edit', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_game))
    res = self.client().post("api/v1/results/1/new", headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(result))
    res = self.client().get("api/v1/players/1", headers={'Content-Type': 'application/json', 'api-token': api_token} )
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('rank_points'), 45)

  def test_player_can_update_their_name(self):
    updated_name = {
      "first_name": "Bobby"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player2))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().patch('api/v1/players/my_profile', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_name))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('email'), 'bob@test.com')
    self.assertEqual(json_data.get('first_name'), 'Bobby')

  def test_player_can_update_their_password(self):
    updated_player = {
      "password": "password2",
      "ability": "Intermediate"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player2))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().patch('api/v1/players/my_profile', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_player))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    print(json_data)
    self.assertEqual(json_data.get('email'), 'bob@test.com')
    self.assertEqual(json_data.get('ability'), 'Intermediate')

  def test_postcode_distances(self):
    self.assertEqual(PlayerModel.get_distance_between_postcodes("N65HQ", 'EC1M4DT'), 6.764520984238515)

  def test_player_location(self):
    self.assertEqual(PlayerModel.get_player_location("N65HQ"), "Haringey")

  def tearDown(self):
    """
    Runs at the end of the test case; drops the db
    """
    with self.app.app_context():
      db.session.remove()
      db.drop_all()

if __name__ == "__main__":
  unittest.main()
