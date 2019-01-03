from typing import List

from game_logic import session_factory
from game_logic.models.guess import Guess
from game_logic.models.player import Player


def get_game_history(game_id: str) -> List[Guess]:
    session = session_factory.create_session()

    query = session.query(Guess)\
        .filter(Guess.game_id == game_id)\
        .order_by(Guess.guess_count)\
        .all()

    guesses = list(query)

    session.close()

    return guesses


def is_game_over(game_id: str) -> bool:
    history = get_game_history(game_id)
    return any([h.is_correct_guess for h in history])


def get_player_highest_score(player: Player.id) -> List:
    session = session_factory.create_session()

    high_scores = []

    query = session.query(Guess)\
        .filter(Guess.player_id == player)\
        .filter(Guess.is_correct_guess)\
        .order_by(Guess.guess_count)\
        .all()

    high_score = list(query)

    for item in high_score:
        high_scores.append(item.guess_count)

    high_scores.sort()

    session.close()

    if not high_scores:
        high_scores.append(101)

    return high_scores[0]


def get_player_five_high_scores(player: Player.id) -> List:
    session = session_factory.create_session()

    high_scores = []

    query = session.query(Guess)\
        .filter(Guess.player_id == player)\
        .filter(Guess.is_correct_guess)\
        .order_by(Guess.guess_count)\
        .all()

    high_score = list(query)

    for item in high_score:
        high_scores.append(item.guess_count)

    high_scores.sort()

    session.close()

    return high_scores[:5]


def find_player(name: str) -> Player:
    session = session_factory.create_session()

    player = session.query(Player).filter(Player.name == name).first()
    session.close()

    return player


def create_player(name: str) -> Player:
    session = session_factory.create_session()

    player = session.query(Player).filter(Player.name == name).first()
    if player:
        raise Exception("Player already exists")

    player = Player()
    player.name = name
    session.add(player)
    session.commit()

    player = session.query(Player).filter(Player.name == name).first()
    session.close()

    return player


def all_players() -> List[Player]:
    session = session_factory.create_session()

    players = list(session.query(Player).all())
    session.close()
    return players


def record_guess(player: Player, guess_number: int, game_id: str,
                 is_correct_guess: bool, is_hi: bool, guess_count: int,
                 the_number: int):
    session = session_factory.create_session()

    guess = Guess()
    guess.player_id = player.id
    guess.guess = guess_number
    guess.game_id = game_id
    guess.is_correct_guess = is_correct_guess
    guess.is_hi = is_hi
    guess.guess_count = guess_count
    guess.the_number = the_number
    session.add(guess)

    session.commit()
    session.close()


if __name__ == "__main__":
    print(get_player_five_high_scores(1))
    foo = find_player('John')

    bar = get_game_history('95d8dca6-d70f-404f-8768-7a5c297cceda')

    print([x.guess for x in bar])
