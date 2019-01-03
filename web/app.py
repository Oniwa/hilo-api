import flask

from views import game_api, home

app = flask.Flask(__name__)


def main():
    build_views()
    run_web_app()


def build_views():
    game_api.build_views(app)
    home.build_views(app)


def run_web_app():
    app.run(debug=True)


if __name__ == "__main__":
    main()
