import random
import uuid

import flask

from game_logic import game_services
from game_logic.game import GameRound

app = flask.Flask(__name__)


def main():
    run_web_app()


def run_web_app():
    app.run(debug=True)


@app.route('/')
def index():
    return "Hello world!!!"


@app.route('/api/test', methods=['GET'])
def api_test():
    data ={
        'name': 'Micheal',
        'day': 97
    }
    return flask.jsonify(data)


@app.errorhandler(404)
def not_found(_):
    return flask.Response("The page was not found.", status=404)


@app.route('/api/game/users/<user>', methods=['GET'])
def find_user(user: str):
    player = game_services.find_player(user)
    if not player:
        flask.abort(404)
    return flask.jsonify(player.to_json())


@app.route('/api/game/users', methods=['PUT'])
def create_user():
    try:
        if not flask.request.json \
                or 'user' not in flask.request.json \
                or not flask.request.json.get('user'):
            raise Exception("Invalid request: no value for user.")

        username = flask.request.json.get('user').strip()
        player = game_services.create_player(username)

        return flask.jsonify(player.to_json())

    except Exception as x:
        flask.abort(flask.Response(
            response=f"Invalid request: {x}",
            status=400
        ))


@app.route('/api/game/game', methods=['POST'])
def create_game():
    return flask.jsonify({'game_id': str(uuid.uuid4())})


@app.route('/api/game/<game_id>/status', methods=['GET'])
def game_status(game_id: str):
    is_over = game_services.is_game_over(game_id)
    history = game_services.get_game_history(game_id)

    if not history:
        flask.abort(404)

    player = history[0].player_id
    the_number = history[0].the_number
    guess_count = len(history)

    data = {
        'is_over': is_over,
        'player': player,
        'guesses': [h.guess for h in history],
        'guess_count': guess_count,
        'the_number': the_number,
    }

    return flask.jsonify(data)


@app.route('/api/game/users/<user>/top_scores', methods=['GET'])
def player_top_scores(user):
    player = game_services.find_player(user)
    top_player_scores = game_services.get_player_five_high_scores(player.id)

    data = {
        'name': player.name,
        'top scores': top_player_scores
    }
    return flask.jsonify(data)


@app.route('/api/game/top_scores', methods=['GET'])
def top_scores():
    players = game_services.all_players()
    wins = [
        {'player': p.to_json(),
         'score': game_services.get_player_highest_score(p.id)}
        for p in players
    ]

    wins.sort(key=lambda wn: -wn.get('score'))
    return flask.jsonify(wins[:10])


def validate_round_request():
    if not flask.request.json:
        raise Exception("Invalid request: no JSON body.")
    game_id = flask.request.json.get('game_id')
    if not game_id:
        raise Exception("Invalid request: No game_id value")
    user = flask.request.json.get('user')
    if not user:
        raise Exception("Invalid request: No user value")
    db_user = game_services.find_player(user)
    if not db_user:
        raise Exception("Invalid request: No user with name {}".format(user))
    guess = flask.request.json.get('guess')
    if not guess:
        raise Exception("Invalid request: No guess value")

    is_over = game_services.is_game_over(game_id)
    if is_over:
        raise Exception("This game is already over.")

    return db_user, game_id, guess


def get_the_number():
    history = game_services.get_game_history(flask.request.json.get('game_id'))

    if history:
        the_number = history[0].the_number
    else:
        the_number = random.randint(0, 100)

    return the_number


@app.route('/api/game/play_round', methods=['POST'])
def play_round():
    try:
        db_user, game_id, guess = validate_round_request()
        the_number = get_the_number()

        game = GameRound(game_id, db_user, guess, the_number)
        game.play()

        return flask.jsonify({
            'guess': guess,
            'player': db_user.to_json(),
            'is_correct_guess': game.is_correct_guess,
            'round_number': game.guess_count,
            'is_hi': game.is_hi,
            'the_number': game.the_number,
        })
    except Exception as x:
        flask.abort(flask.Response(response=f'Invalid request: {x}',
                                   status=400))


if __name__ == "__main__":
    main()
