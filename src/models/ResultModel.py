import datetime
from . import db # import db instance from models/__init__.py
from marshmallow import fields, Schema


class ResultModel(db.Model): # ResultModel class inherits from db.Model
    """
    Result Model
    """

    # table name
    __tablename__ = 'results' # name our table Results

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False, unique=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    loser_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    result_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    winner = db.relationship("PlayerModel", primaryjoin = "ResultModel.winner_id == PlayerModel.id", backref="winner")
    loser = db.relationship("PlayerModel", primaryjoin = "ResultModel.loser_id == PlayerModel.id", backref="loser")
    game = db.relationship("GameModel", back_populates="result")


    def __init__(self, data): # class constructor used to set the class attributes
        """
        Class constructor: set class attributes
        """
        self.game_id = data.get('game_id')
        self.winner_id = data.get('winner_id')
        self.loser_id = data.get('loser_id')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    # def update(self, data):
    #     for key, item in data.items():
    #         setattr(self, key, item)
    #     self.modified_at = datetime.datetime.utcnow()
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()

    # @staticmethod
    # def get_all_results():
    #     return ResultModel.query.all()

    # @staticmethod
    # def get_one_result(id):
    #     return ResultModel.query.get(id)

    @staticmethod
    def get_result_by_game(value):
        return ResultModel.query.filter_by(game_id=value).first()

    @staticmethod
    def get_all_results(value):
        return ResultModel.query.filter_by(game_id=value)


    def __repr__(self):
        return '<id {}>'.format(self.id)

class ResultSchema(Schema):
    """
    Result Schema
    """
    id = fields.Int(dump_only=True)
    game_id = fields.Int(required=True)
    winner_id = fields.Int(required=False)
    loser_id = fields.Int(required=False)
    result_confirmed = fields.Boolean(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
