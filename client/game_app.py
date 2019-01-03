from api import GameService


def check_guess(is_hi:bool, is_over: bool, name: str,
                guess: int, guess_count: int):
    if not is_over:
        if is_hi:
            print(f'Sorry {name}, your guess of {guess} '
                  f'was too HIGH.\n')
        else:
            print(f'Sorry {name}, your guess of {guess}'
                  f' was too LOW.\n')
    else:
        print(f'Excellent work {name}, you won in'
              f' {guess_count} guesses, the number was {guess}!\n')

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

    if not player:
        svc.create_user(user=player_name)
        player = svc.find_user(player_name)

    name = player.json().get('name')

    player_scores = svc.player_top_scores(name).json().get('top scores')

    player_scores = ', '.join(str(x) for x in player_scores)
    print(f'\n{name}\'s best scores are {player_scores}\n')

    is_over = False
    while not is_over:
        guess = int(input('Guess a number: '))
        rnd = svc.play_round(game_id=game_id, user=name, guess=guess)
        is_hi = rnd.json().get('is_hi')
        is_over = rnd.json().get('is_correct_guess')
        round_number = rnd.json().get('round_number')
        check_guess(is_hi, is_over, name, guess, round_number)


if __name__ == "__main__":
    main()
