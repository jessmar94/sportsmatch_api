import unittest
import os
import json
from ..app import create_app, db

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
      "gender": "M",
      "dob": "1990-01-01",
      "ability": "Beginner"
    }

    with self.app.app_context():
      db.create_all()

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

  def test_player_login(self):
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    self.assertEqual(res.status_code, 201)
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    json_data = json.loads(res.data)
    self.assertTrue(json_data.get('jwt_token'))
    self.assertEqual(res.status_code, 200)

  def test_error_when_player_login_with_invalid_password(self):
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    self.assertEqual(res.status_code, 201)
    invalid_password_player = {
      "email": "dom@test.com",
      "password": "password!"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(invalid_password_player))
    json_data = json.loads(res.data)
    self.assertFalse(json_data.get('jwt_token'))
    self.assertEqual(json_data.get('error'), 'invalid credentials')
    self.assertEqual(res.status_code, 400)

  def test_error_when_player_login_with_invalid_email(self):
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    self.assertEqual(res.status_code, 201)
    invalid_password_player = {
      "email": "dom@te.com",
      "password": "password"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(invalid_password_player))
    json_data = json.loads(res.data)
    self.assertFalse(json_data.get('jwt_token'))
    self.assertEqual(json_data.get('error'), 'invalid credentials')
    self.assertEqual(res.status_code, 400)

  def test_player_can_view_their_own_profile(self):
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    self.assertEqual(res.status_code, 201)
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().get('api/v1/players/my_profile', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('email'), 'dom@test.com')
    self.assertEqual(json_data.get('first_name'), 'Dom')

  def test_player_can_update_their_own_profile(self):
    updated_player = {
      "first_name": "Dominic"
    }
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    self.assertEqual(res.status_code, 201)
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().patch('api/v1/players/my_profile', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_player))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('email'), 'dom@test.com')
    self.assertEqual(json_data.get('first_name'), 'Dominic')

  def test_player_can_delete_their_account(self):
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    self.assertEqual(res.status_code, 201)
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().delete('api/v1/players/my_profile', headers={'Content-Type': 'application/json', 'api-token': api_token})
    self.assertEqual(res.status_code, 204)
  
  def tearDown(self):
    """
    Runs at the end of the test case; drops the db
    """
    with self.app.app_context():
      db.session.remove()
      db.drop_all()

if __name__ == "__main__":
  unittest.main()