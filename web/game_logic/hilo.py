import random
import uuid

from game_logic import game_services as gs

print('---------------------------------')
print('   GUESS THAT NUMBER GAME')
print('---------------------------------')
print()

the_number = random.randint(0, 100)
guess = -1

name = input('Player what is your name? ')
player = gs.find_or_create_player(name)
high_scores = gs.get_player_five_high_scores(player.id)
high_scores = ', '.join(str(x) for x in high_scores)
print(f'{player.name}\'s best scores are {high_scores}')

game_id = str(uuid.uuid4())

count = 0
while guess != the_number:
    guess_text = input('Guess a number between 0 and 100: ')
    guess = int(guess_text)
    count += 1

    if guess < the_number:
        # print('Your guess of ' + guess + ' was too LOW.')
        gs.record_guess(player=player, guess_number=guess, game_id=game_id,
                        is_correct_guess=False, is_hi=False, guess_count=count,
                        the_number=the_number)
        print(f'Sorry {name}, your guess of {guess} was too LOW.')
    elif guess > the_number:
        gs.record_guess(player=player, guess_number=guess, game_id=game_id,
                        is_correct_guess=False, is_hi=True, guess_count=count,
                        the_number=the_number)
        print(f'Sorry {name}, your guess of {guess} was too HIGH.')
    else:
        gs.record_guess(player=player, guess_number=guess, game_id=game_id,
                        is_correct_guess=True, is_hi=False, guess_count=count,
                        the_number=the_number)
        print(f'Excellent work {name}, you won in {count} guesses,'
              f' it was {guess}!')
