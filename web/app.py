import uuid

import flask

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
    return "The page was not found."


@app.route('/api/game/users/<user>', methods=['GET'])
def find_user(user: str):
    # TODO: Implement
    return f"Would find user {user}."


@app.route('/api/game/users/', methods=['PUT'])
def create_user(user: str):
    # TODO: Implement
    return f"Would crete user {user}."


@app.route('/api/game/game', methods=['POST'])
def create_game():
    return flask.jsonify({'game_id': str(uuid.uuid4())})


@app.route('/api/game/<game_id>/status', methods=['GET'])
def game_status(game_id: str):
    # TODO: Implement
    return f"Would return status for game {game_id}"


@app.route('/api/game/users/<user>/top_scores', methods=['GET'])
def player_top_scores(user):
    # TODO: Implement
    return f'Would return top five scores for {user}'


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
