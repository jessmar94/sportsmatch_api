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
          "gender": "Male",
          "dob": "1990-01-01",
          "ability": "Beginner",
          "postcode": "N65HQ",
          "rank_points": 50
        }
        self.player_2 = {
          "first_name": "Pam",
          "last_name": "M",
          "email": "pam@test.com",
          "password": "password",
          "gender": "Female",
          "dob": "1990-01-01",
          "ability": "Beginner",
          "postcode": "N65SQ",
          "rank_points": 50
        }
        self.game_1 = {
          "organiser_id": 1,
          "opponent_id": 2,
          "status": "pending",
          "game_date": "2019-11-01",
          "game_time": "15:00:00"
        }
        self.game_2 = {
          "organiser_id": 1,
          "opponent_id": 2,
          "status": "pending",
          "game_date": "2020-10-20",
          "game_time": "19:00:00"
        }

        with self.app.app_context():
            db.create_all()
            player1 = PlayerModel(self.player_1)
            db.session.add(player1)
            db.session.commit()
            db.session.refresh(player1)
            player1_id = player1.id

            player2 = PlayerModel(self.player_2)
            db.session.add(player2)
            db.session.commit()
            db.session.refresh(player2)
            player2_id = player2.id

            game1 = GameModel(self.game_1)
            db.session.add(game1)
            db.session.commit()
            db.session.refresh(game1)
            game1_id = game1.id

            game2 = GameModel(self.game_2)
            db.session.add(game2)
            db.session.commit()
            db.session.refresh(game2)
            game2_id = game2.id


        self.result_1 = {
          "game_id": game1_id,
          "winner_id": player1_id,
          "loser_id": player2_id,
          "result_confirmed": True
        }

        self.result_2 = {
          "game_id": game1_id,
          "winner_id": player2_id,
          "loser_id": player1_id,
          "result_confirmed": True
        }

    def test_return_of_games_with_results_for_organiser(self):
          updated_game = {
            "status": "confirmed"
          }
          res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
          api_token = json.loads(res.data).get('jwt_token')
          res = self.client().patch('api/v1/games/1/edit', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_game))
          json_data = json.loads(res.data)
          res = self.client().post("api/v1/results/1/new", headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.result_1))
          json_data = json.loads(res.data)
          res = self.client().get('api/v1/games/organiser', headers={'Content-Type': 'application/json', 'api-token': api_token})
          json_data = json.loads(res.data)
          print(json_data)
          self.assertEqual(json_data[0].get('winner_id'), 1)
          self.assertEqual(res.status_code, 200)


    def test_organiser_creates_result(self):
          updated_game = {
            "status": "confirmed"
          }
          res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
          api_token = json.loads(res.data).get('jwt_token')
          res = self.client().patch('api/v1/games/1/edit', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_game))
          json_data = json.loads(res.data)
          res = self.client().post("api/v1/results/1/new", headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.result_1))
          json_data = json.loads(res.data)
          self.assertEqual(res.status_code, 201)

    def test_cannot_create_result_if_opponent(self):
          updated_game = {
            "status": "confirmed"
          }
          res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_2))
          api_token = json.loads(res.data).get('jwt_token')
          res = self.client().patch('api/v1/games/1/edit', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_game))
          json_data = json.loads(res.data)
          res = self.client().post('api/v1/results/1/new', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.result_1))
          self.assertEqual(res.status_code, 400)

    def test_cannot_create_result_pending_game(self):
          res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
          api_token = json.loads(res.data).get('jwt_token')
          res = self.client().post('api/v1/results/1/new', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.result_1))
          self.assertEqual(res.status_code, 400)

    def test_cannot_create_two_results(self):
          updated_game = {
            "status": "confirmed"
          }
          res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
          api_token = json.loads(res.data).get('jwt_token')
          res = self.client().patch('api/v1/games/1/edit', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_game))
          json_data = json.loads(res.data)
          res = self.client().post("api/v1/results/1/new", headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.result_1))
          json_data = json.loads(res.data)
          res = self.client().post("api/v1/results/1/new", headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.result_2))
          json_data = json.loads(res.data)
          self.assertEqual(res.status_code, 400)

    def tearDown(self):
        """
        Runs at the end of the test case; drops the db
        """
        with self.app.app_context():
          db.session.remove()
          db.drop_all()

if __name__ == "__main__":
    unittest.main()
