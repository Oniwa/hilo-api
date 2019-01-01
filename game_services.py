from typing import List

from data import session_factory
from models.guess import Guess
from models.player import Player




def get_game_history(game_id: str) -> List[Guess]:
    session = session_factory.create_session()

    query = session.query(Guess)\
        .filter(Guess.game_id == game_id)\
        .order_by(Guess.guess_count)\
        .all()

    guesses = list(query)

    session.close()

    return guesses


def get_player_high_score(player: Player) -> int:
    session = session_factory.create_session()

    query = session.filter(Guess)\
        .filter(Guess.player_id == player)\
        .filter(Guess.is_correct_guess)\
        .order_by(Guess.guess_count)\
        .all()

    high_score = min(query)

    session.close()

    return high_score


def find_or_create_player(name: str) -> Player:
    session = session_factory.create_session()

    player = session.query(Player).filter(Player.name == name).first()
    if player:
        session.close()
        return player

    player = Player()
    player.name = name
    session.add(player)
    session.commit()

    player = session.query(Player).filter(Player.name == name).first()
    return player


def all_players() -> List[Player]:
    session = session_factory.create_session()

    players = list(session.query(Player).all())
    session.close()
    return players


def record_guess(player, guess_number: int, game_id: str,
                 is_correct_guess: bool, is_hi: bool, guess_count: int):
    session = session_factory.create_session()

    guess = Guess()
    guess.player_id = player.id
    guess.guess = guess_number
    guess.game_id = game_id
    guess.is_correct_guess = is_correct_guess
    guess.is_hi = is_hi
    guess.guess_count = guess_count
    session.add(guess)

    session.commit()
    session.close()