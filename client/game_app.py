from api import GameService


def main():
    svc = GameService()

    print("Game app! (client)")
    print()
    print()
    print("TOP SCORES")
    for s in svc.top_scores().json():
        print(f'{s.get("player").get("name")} scored {s.get("score")}')
    print()

    game_id = svc.create_game().json().get('game_id')

    player_name = input('What is your name? ')

    player = svc.find_user(player_name)
    print(player)
    if not player:
        svc.create_user(user=player_name)
        player = svc.find_user(player_name)

    print(player.json())

    # is_over = False
    # while not is_over:
    #     name = player.get('name')
    #     guess = input('Guess a number: ')
    #     rnd = svc.play_round(game_id=game_id, user)

if __name__ == "__main__":
    main()
