import unittest
import os
import json
from ..models.MessageModel import MessageModel, MessageSchema
from ..models.PlayerModel import PlayerModel, PlayerSchema
from ..app import create_app, db
from ..shared.Authentication import Auth
from datetime import datetime, timedelta

class MessageTest(unittest.TestCase):
    """
    Message Test Case
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

        self.message_1 = {
          "sender_id": player_1_id,
          "receiver_id": player_2_id,
          "content": "this is a message"
        }

    def test_message_created(self):
        res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().post('api/v1/messages/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.message_1))
        json_data = json.loads(res.data)
        self.assertEqual(json_data.get('sender_id'), 1)
        self.assertEqual(json_data.get('receiver_id'), 2)
        self.assertEqual(json_data.get('content'), "this is a message")
