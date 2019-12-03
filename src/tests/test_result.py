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
          "ability": "Beginner",
          "postcode": "n169np"
        }
        self.player_2 = {
          "first_name": "Pam",
          "last_name": "M",
          "email": "pam@test.com",
          "password": "password",
          "gender": "F",
          "dob": "1990-01-01",
          "ability": "Beginner",
          "postcode": "n169np"
        }
        self.game_1 = {
          "organiser_id": 1,
          "opponent_id": 2,
          "confirmed": "true",
          "game_date": "2019-01-01",
          "game_time": "15:00:00"
        }
        self.game_2 = {
          "organiser_id": 1,
          "opponent_id": 2,
          "confirmed": "true",
          "game_date": "2019-11-01",
          "game_time": "15:00:00"
        }
        self.game_3 = {
          "organiser_id": 2,
          "opponent_id": 1,
          "confirmed": "true",
          "game_date": "2019-12-01",
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

            game3 = GameModel(self.game_3)
            db.session.add(game3)
            db.session.commit()
            db.session.refresh(game3)
            game3_id = game3.id


        self.result_1 = {
          "game_id": game1_id,
          "winner_id": player2_id,
          "loser_id": player1_id,
          "result_confirmed": "False"
        }
        self.result_2 = {
          "game_id": game2_id,
          "winner_id": player1_id,
          "loser_id": player2_id,
          "result_confirmed": "False"
        }
        self.result_3 = {
          "game_id": game3_id,
          "winner_id": player1_id,
          "loser_id": player2_id,
          "result_confirmed": "False"
        }

    # def test_create_a_result(self):
    #     res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
    #     api_token = json.loads(res.data).get('jwt_token')
    #     res = self.client().post('api/v1/results/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.result_1))
    #     self.assertEqual(res.status_code, 201)

    # def test_player_can_view_all_their_results(self):
    #     res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
    #     api_token = json.loads(res.data).get('jwt_token')
    #     res = self.client().post('api/v1/results/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.result_1))
    #     res = self.client().post('api/v1/results/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.result_2))
    #     res = self.client().get('api/v1/results/', headers={'Content-Type': 'application/json', 'api-token': api_token})

    #     self.assertEqual(res.status_code, 200)
    #     json_data = json.loads(res.data)
    #     print(json_data)
    #     self.assertEqual(json_data[0].get('winner_id'), 2)
        # self.assertEqual(json_data[1].get('winner_id'), 1)

    # def test_player_can_edit_their_results(self):
    #     edited_result = {
    #       "winner_id": 1,
    #       "loser_id": 2
    #     }
    #     res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
    #     api_token = json.loads(res.data).get('jwt_token')
    #     res = self.client().post('api/v1/results/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.result_1))
    #     res = self.client().patch('api/v1/results/1/edit', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(edited_result))
    #     json_data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 201)
    #     self.assertEqual(json_data.get('winner_id'), 1)
    #     self.assertNotEqual(json_data.get('loser_id'), 1)

    # def test_error_when_not_organiser_tries_to_edit_result(self):
    #     edited_result = {
    #       "winner_id": 1,
    #       "loser_id": 2
    #     }
    #     res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_2))
    #     api_token = json.loads(res.data).get('jwt_token')
    #     res = self.client().post('api/v1/results/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.result_3))
    #     res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
    #     api_token = json.loads(res.data).get('jwt_token')
    #     res = self.client().patch('api/v1/results/1/edit', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(edited_result))
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(json.loads(res.data).get('error'), 'only organiser can edit the result')

    # def test_error_if_result_not_found(self):
        # edited_result = {
        #   "winner_id": 2,
        #   "loser_id": 1
        # }
        # res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
        # api_token = json.loads(res.data).get('jwt_token')
        # res = self.client().patch('api/v1/results/1/edit', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(edited_result))
        # self.assertEqual(res.status_code, 404)
        # self.assertEqual(json.loads(res.data).get('error'), 'result not found')

    def tearDown(self):
        """
        Runs at the end of the test case; drops the db
        """
        with self.app.app_context():
          db.session.remove()
          db.drop_all()

if __name__ == "__main__":
    unittest.main()
