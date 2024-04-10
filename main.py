from random import shuffle
import re
import typer
from typing_extensions import Annotated
import operator
from os.path import exists


MAX_PLAYERS = 26
MIN_PLAYERS = 1


def get_words(filepath, num_of_words):
    if not num_of_words == 0:
        with open(filepath) as input_file:
            words = [next(input_file) for _ in range(num_of_words)]
    else:
        file = open(filepath, 'r')
        words = file.readlines()
        file.close()
    shuffle(words)
    words = ' '.join(words)
    return re.sub(r'[^a-zA-Z ]', '', words.lower())


def obscure_phrase(guess, word, guessed):
    printed_result = ''
    score = 0
    for s in word:
        if guess == s:
            printed_result = printed_result + s
            score = score + 1
        elif s in guessed:
            printed_result = printed_result + s
        elif s == " ":
            printed_result = printed_result + " "
        else:
            printed_result = printed_result + '-'
    return [printed_result, score]


def next_player(current_player, num_of_players):
    if current_player == num_of_players - 1:
        return 0
    else:
        return current_player + 1


def print_scores(players_score, player_names):
    for index in players_score:
        print("{} score is {}".format(player_names[index], players_score[index]))


def is_game_end(players_score, word):
    num_of_spaces = operator.countOf(word, " ")
    return sum(players_score.values()) == len(word) - num_of_spaces


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def print_winner(players_score, player_names):
    top_score = max(players_score.values())
    keys = [str(k + 1) for k, v in players_score.items() if v == top_score]
    winners = ', '.join(keys)
    if len(keys) > 1:
        print("players {} are the winners!!!".format(rreplace(winners, ', ', ' and ', 1)))
    else:
        print("{} is the winner!".format(rreplace(player_names[int(winners) - 1], ', ', ' and ', 1)))


def start_game(players_score, num_of_players, filepath, num_of_words):
    # get a random word
    word = get_words(filepath, num_of_words)
    guessed = []
    player_names = [""] * num_of_players
    # init player names
    for i in range(num_of_players):
        player_names[i] = typer.prompt('Player {}, please enter your name'.format(i + 1))

    current_player_index = 0
    while True:
        print("used letters: {}".format(guessed))
        player_letter = typer.prompt("{}, please guess a letter".format(player_names[current_player_index]))
        while True:
            if len(player_letter) == 1:  # only 1 letter per guess
                if not player_letter.isalpha():  # the user entered an invalid letter (such as number or a sign)
                    player_letter = typer.prompt('Guesses should be LETTERS only. Try again')
                    continue
                elif player_letter in guessed:  # this letter has already been guessed
                    player_letter = typer.prompt('{} has already been guessed. Try again'.format(player_letter))
                    continue
                else:
                    player_letter = player_letter.lower()
                    break
            else:
                player_letter = typer.prompt('Guesses should be only 1 letter. Try again')

        guessed.append(player_letter)
        (print_result, additional_score) = obscure_phrase(player_letter, word, guessed)
        print(print_result)
        print()
        players_score[current_player_index] += additional_score
        print_scores(players_score, player_names)
        if is_game_end(players_score, word):
            print_winner(players_score, player_names)
            print("The game as ended")
            return
        else:
            current_player_index = next_player(current_player_index, num_of_players)


def main(filepath: Annotated[str, typer.Argument(help="path to the words list file")], numofwords: Annotated[int, typer.Option(help="number of words to play with")] = 0
):
    if not exists(filepath):
        print("wrong file path. try again.")
        return 1
    print('Lets Play!!')
    while True:
        try:
            num_of_players = int(typer.prompt('How many players'))
            players_score = [0] * num_of_players
            players_score = {index: element for index, element in enumerate(players_score)}
            if not MIN_PLAYERS <= num_of_players <= MAX_PLAYERS:
                raise ValueError  # this will send it to the print message and back to the input option
            break
        except ValueError:
            print("Invalid integer. The number must be in the range of {}-{}.".format(MIN_PLAYERS, MAX_PLAYERS))

    start_game(players_score, num_of_players, filepath, numofwords)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    typer.run(main)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
