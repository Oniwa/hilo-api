import uplink


@uplink.json
class GameService(uplink.Consumer):
    def __init__(self):
        super().__init__(base_url='http://localhost:5000')

    @uplink.put('api/game/users')
    def create_user(self, **kwargs: uplink.Body):
        pass

    @uplink.get('api/game/users/{username}')
    def find_user(self, username):
        pass

    @uplink.post('api/game/game')
    def create_game(self, **kwargs: uplink.Body):
        pass

    @uplink.get('api/game/{game_id}/status')
    def game_status(self, game_id):
        pass

    @uplink.get('api/users/{user}/top_scores')
    def player_top_scores(self, user):
        pass

    @uplink.get('api/game/top_scores')
    def top_scores(self):
        pass

    @uplink.post('api/game/play_round')
    def play_round(self, **kwargs: uplink.Body):
        pass
