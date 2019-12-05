import unittest
import json
from ..app import create_app, db
from ..models.MessageModel import MessageModel
from ..models.PlayerModel import PlayerModel, PlayerSchema
from ..models.GameModel import GameModel, GameSchema


class MessageTest(unittest.TestCase):
    """
    Message Test Case
    """
    def setUp(self):
        """
        Runs before each test case method: creates the app and db tables.
        """
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
        # self.game_2 = {
        #   "organiser_id": 1,
        #   "opponent_id": 2,
        #   "status": "pending",
        #   "game_date": "2020-10-20",
        #   "game_time": "19:00:00"
        # }

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
            self.game1_id = game1.id
            game1_organiser = game1.organiser_id
            game1_opponent = game1.opponent_id

            # game2 = GameModel(self.game_2)
            # db.session.add(game2)
            # db.session.commit()
            # db.session.refresh(game2)
            # game2_id = game2.id
            # game2_organiser = game2.organiser_id
            # game2_opponent = game2.opponent_id

        self.message_1 = {
          "game_id": self.game1_id,
          "organiser_id": game1_organiser,
          "opponent_id": game1_opponent,
          "sender_id": game1_organiser,
          "content": "Hey want to play a game of ball?"
        }

        self.message_2 = {
          "game_id": self.game1_id,
          "organiser_id": game1_organiser,
          "opponent_id": game1_opponent,
          "sender_id": game1_organiser,
          "content": "Yeah man what time?"
        }

    def message(self):
        res = self.client().post('api/v1/players/login',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.player_1))
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().post('api/v1/messages/',
                                 headers={'Content-Type': 'application/json',
                                          'api-token': api_token},
                                 data=json.dumps(self.message_1))
        json_data = json.loads(res.data)
        self.assertEqual(json_data.get('content'), "Hey want to play a game of ball?")
        self.assertEqual(res.status_code, 201)

    def test_return_one_game(self):
        res = self.client().post('api/v1/players/login',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.player_1))
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().post('api/v1/messages/',
                                 headers={'Content-Type': 'application/json',
                                          'api-token': api_token},
                                 data=json.dumps(self.message_1))
        json_data = json.loads(res.data)
        self.assertEqual(json_data.get('content'), "Hey want to play a game of ball?")
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
