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
    guess = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    guess_count = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    player_id = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    is_hi = sqlalchemy.Column(sqlalchemy.Boolean, index=True, default=False)
    is_correct_guess = sqlalchemy.Column(sqlalchemy.Boolean, index=True,
                                         default=False)
    the_number = sqlalchemy.Column(sqlalchemy.Integer, index=True)
