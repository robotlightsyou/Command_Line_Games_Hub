#!/usr/bin/python3
'''
DOCSTRING: This program serves as a hub for simple command line games.
Ideally games can be run independently or from here.
    Input:
        no input
    Output:
        no output, but can start games and write to memory.
'''

import random
import time
import os
from pprint import pprint
import shelve
import dicts
#from . import dicts
#from dicts import EOSDICT as eos
import memory as m

DECKSDICT = dicts.DICTS_DICT
DECKLIST = list(DECKSDICT.keys())

# add times correct attribute


class Term():
    def __init__(self, name, shared_dict):
        self.name = name
        self .dict_name = shared_dict['__dict_name__']
        self.defi = shared_dict[name]
        self.times_answeered = 0
        self.avg_time = 0
        self.cum_time = 0

    def update_time(self, start_time, end_time):
        ans_time = end_time - start_time
        self.times_answeered += 1
        self.cum_time += ans_time
        self.avg_time = self.cum_time / self.times_answeered

    def print_stats(self):
        print(self.__str__())
        print("Times answered: {}".format(self.times_answeered))
        print("Average Time: {:.1f}".format(self.avg_time))

    def __str__(self):
        return "'{}': {}".format(self.name, self.defi)


class User():
    def __init__(self, name):
        self.name = name
        self.memory = {}

    # rewrite so any deck name can be added
    def add_deck(self, deck):
        for card in deck.keys():
            self.memory[card] = Term(card, dicts.EOSDICT)


def main():
    games_list = ['Player Stats', 'Memory']
    # player = get_player()
    # game_cards = []
    # game_cards.extend(m.memory(player))
    # play_again(player)
    # return_stats(player, set(game_cards))
    # save_player(player)
    player = get_player()
    game_cards = []
    game_cards = ['go', 'order 66', 'address']
    game = choose_list(games_list)
    if game == 'Player Stats':
        return_stats(player, set(game_cards))
    elif game == 'Memory':
        deck = dicts.DICTS_DICT[choose_list(DECKLIST)]
        print(deck['__dict_name__'])
        game_cards = ['patch', 'macro', 'address']
        # game_cards = game_cards.extend(m.memory(player, deck))
    return_stats(player, set(game_cards))
    save_player(player)


def choose_game(games_list):
    print('Enter the number for the game you want to play.')
    for index, value in enumerate(games_list):
        print(str(index + 1) + ') {}'.format(value))
    print()
    response = valifate_response(games_list)
    return games_list[response]


def choose_list(options):
    print('Which deck would you like to play?')
    for index, value in enumerate(options):
        print(str(index + 1) + ') {}'.format(value))
    print()
    response = valifate_response(options)
    return options[response]


def valifate_response(ans_list):
    '''
    DOCSTRING: This function actually gets the user's response and
    tests that it is one of the valid options
    Input:
    Output:
        integer: response
    '''
    response = -1
    while response not in list(range(len(ans_list))):
        try:
            response = int(input('>')) - 1
        except ValueError:
            print("Please emter a valid response")
    # while response not in [1, 2, 3, 0]:
    if (response) not in list(range(len(ans_list))):
        print("Please emter a valid response")
        response = valifate_response(ans_list)
    return response


def play_again(user):
    '''
    DOCSTRING: This function asks the user if they want to play again
    if yes, restart memory, if no then exit.
    Input:
        User: user
    Output:
        No output, but can restart the game
    '''
    print("{},\n\tWould you like to play again?".format(user.name))
    print("Enter 'y' or 'n'")
    if input('>')[0].lower() != 'n':
        m.memory(user)


def return_stats(user, recent_words):
    '''
    DOCSTRING: This function takes in a user and a list of session
    words and prints that users stats with those cards
    Input:
        User: user
        list of strings: recent_words
    Output:
        No output, prints to screen
    '''
    os.system('clear')
    print("In the last session you answered the following cards,")
    print("here's your stats for them:\n")
    for card in recent_words:
        print(user.memory[card].print_stats())
        print()


##################
# Save user data #
##################

def how_long():
    print('Enter how long you would like the round to last in seconds.')
    print('Minimum is 30 seconds, max is 120.\n')
    time = input(">")
    try:
        time = int(time)
        if 30 <= time <= 120:
            return time
        else:
            print("please enter digits between 30-120")
            return how_long()
    except ValueError:
        print("please enter digits between 30-120")
        return how_long()


def get_player():
    print("Are you a returning player?\n[y/n]\n")
    new = input('>')
    if new.lower() == 'n':
        user = new_player()
        user.add_deck(dicts.EOSDICT)
    elif new.lower() == 'y':
        user = load_player()
        # user = load_player()
    else:
        print("Please enter 'y' or 'n'")
        return get_player()
    return user


def save_player(user):
    # @TODO: convert to 'with open' method
    d = shelve.open("myfile")
    d[user.name] = user
    d.close()


def new_player():
    print("Who is playing? ")
    player_name = input('>')
    return User(player_name)


def load_player():
    print("Who is playing? ")
    player_name = input('>')
    d = shelve.open('myfile')
    try:
        user = d[player_name]
    except KeyError:
        d.close()
        return no_name()
    d.close()
    # with open('myfile.db', 'r') as loadfile:
    #    user = loadfile[player_name]
    return user


def no_name():
    print("Sorry, I can't find that file. Would you like to:")
    ans_list = ["Try a different name", "Start a new save"]
    for index, value in enumerate(ans_list):
        print(str(index + 1) + ') {}'.format(value))
    response = valifate_response(ans_list)
    if response == 0:
        return load_player()
    elif response == 1:
        user = new_player()

        # FIX DECK
        user.add_deck(dicts.EOSDICT)
        return user

# @TODO: update comments and documentation
# @TODO: read csv and split entries into dictionary


if __name__ == '__main__':
    main()
