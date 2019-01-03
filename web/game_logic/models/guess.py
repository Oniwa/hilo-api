import datetime

import sqlalchemy

# noinspection PyPackageRequirements
from game_logic.models.model_base import ModelBase


class Guess(ModelBase):
    __tablename__ = 'guesses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    created = sqlalchemy.Column(sqlalchemy.DateTime,
                                default=datetime.datetime.now, index=True)
    game_id = sqlalchemy.Column(sqlalchemy.String, index=True)
    guess = sqlalchemy.Column(sqlalchemy.Integer, index=True)  # Number Guessed
    guess_count = sqlalchemy.Column(sqlalchemy.Integer, index=True)  # Number of Guesses
    player_id = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    is_hi = sqlalchemy.Column(sqlalchemy.Boolean, index=True, default=False)
    is_correct_guess = sqlalchemy.Column(sqlalchemy.Boolean, index=True,
                                         default=False)
    the_number = sqlalchemy.Column(sqlalchemy.Integer, index=True)  # Then hidden number

    def to_json(self):
        return {
            'id': self.id,
            'created': self.created,
            'game_id': self.game_id,
            'guess': self.guess,
            'guess_count': self.guess_count,
            'player_id': self.player_id,
            'is_hi': self.is_hi,
            'is_correct_guess': self.is_correct_guess,
            'the_number': self.the_number
        }