from game_logic import game_services
from game_logic.models.player import Player
from game_logic.models.guess import Guess

class GameRound:
    def __init__(self, game_id: str, db_user: Player, guess: int,
                 the_number: int):
        self.game_id = game_id
        self.player = db_user
        self.guess = guess
        self.the_number = the_number

        history = game_services.get_game_history(self.game_id)
        self.is_correct_guess = game_services.is_game_over(self.game_id)
        self.is_hi = False
        self.guess_count = len(history)

    def play(self):
        if self.is_correct_guess:
            raise Exception("Game is already over, cannot play further")

        self.guess_count += 1

        if self.guess < self.the_number:
            # print('Your guess of ' + guess + ' was too LOW.')
            self.is_correct_guess = False
            self.is_hi = False
            self.guess_count = self.guess_count

            print(f'Sorry {self.player.name}, your guess of {self.guess}'
                  f' was too LOW.')
        elif self.guess > self.the_number:
            self.is_correct_guess = False
            self.is_hi = True
            self.guess_count = self.guess_count

            print(f'Sorry {self.player.name}, your guess of {self.guess} '
                  f'was too HIGH.')
        else:
            self.is_correct_guess = True
            self.is_hi = False
            self.guess_count = self.guess_count

            print(f'Excellent work {self.player.name}, you won in'
                  f' {self.guess_count} guesses, the number was {self.guess}!')

        print('RECORDING GUESS')
        self.record_guess()

    def record_guess(self):
        game_services.record_guess(player=self.player,
                                   guess_number=self.guess,
                                   game_id=self.game_id,
                                   is_correct_guess=self.is_correct_guess,
                                   is_hi=self.is_hi,
                                   guess_count=self.guess_count,
                                   the_number=self.the_number)