import uuid

import flask

from game_logic import game_services

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
    guess_count = max([h.guess_count for h in history])

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
    top_player_scores = game_services.get_player_high_score(player.id)

    data = {
        'name': player.name,
        'top scores': top_player_scores
    }
    return flask.jsonify(data)


@app.route('/api/game/top_scores', methods=['GET'])
def top_scores():
    # TODO: Implement
    return "Would return top scorers"


@app.route('/api/game/play_round', methods=['POST'])
def play_round():
    # TODO: Implement
    return 'Would play a round'


if __name__ == "__main__":
    main()
