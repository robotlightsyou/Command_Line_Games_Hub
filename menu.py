#!/usr/bin/python3
'''
DOCSTRING: This program serves as a hub for simple command line games.
Ideally games can be run independently or from here.
    Input:
        no input
    Output:
        no output, but can start games and write to memory.

#@TODO:
* [ ] - fix play_again so it goes more than 1 deep
        --> skipping straight to displaying stats, in memory, not menu
* [ ] - clean up preint formatting
* [ ] - why is return_stats printing none? nb print(p(vars))
* [ ] - fix add_deck to check if deck exists
* [ ] - add ordered dict to printing dicts.ALL_DECKS
* [ ] - force replay menu after time? nb anslist ran out of cards


* [X] - fix anser/anspad selection so it ignores __dict_name__
* [X] - fix return_stats shows times_correct, update methods
'''

import random
import time
import os
import sys
from pprint import pprint
import shelve
import dicts
import memory as m

DECKSDICT = dicts.ALL_DECKS
DECKLIST = list(DECKSDICT.keys())

# fix updates so that they display  times correct


class Term():
    def __init__(self, name, shared_dict):
        self.name = name
        self .dict_name = shared_dict['__dict_name__']
        self.defi = shared_dict[name]
        self.times_answeered = 0
        self.times_correct = 0
        self.avg_time = 0
        self.cum_time = 0

    def update_time(self, start_time, end_time):
        ans_time = end_time - start_time
        self.times_answeered += 1
        self.cum_time += ans_time
        self.avg_time = self.cum_time / self.times_answeered

    # should be using setattr()?

    def update_correct(self):
        self.times_correct += 1

    def print_stats(self):
        print(self.__str__())
        print("Times answered: {}".format(self.times_answeered))
        print("Times correct: {}".format(self.times_correct))
        print("Average Time: {:.1f}".format(self.avg_time))

    def __str__(self):
        return "'{}': {}".format(self.name, self.defi)


class User():
    def __init__(self, name):
        self.name = name
        self.memory = {}
        self.memory_decks = []

    # rewrite so any deck name can be added
    def add_deck(self, deck):
        name = deck['__dict_name__']
        if name not in self.memory_decks:
            self.memory_decks.append(name)
            self.memory[name] = {}
            for card in deck.keys():
                self.memory[name][card] = Term(card, deck)


def choose_list(options):
    print('Which option would you like?')
    for index, value in enumerate(options):
        print(str(index + 1) + ') {}'.format(value))
    print()
    response = valifate_response(options)
    print()
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
    if (response) not in list(range(len(ans_list))):
        print("Please emter a valid response")
        response = valifate_response(ans_list)
    return response


def play_again(user, deck):
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
        m.memory(user, deck)

# fix so displays times correct primarily


def return_stats(user, recent_words, deck):
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
    print("{},".format(user.name))
    print("    In the last session you answered the following cards,")
    print("here's your stats for them:\n")
    for card in recent_words:
        print(user.memory[deck['__dict_name__']][card].print_stats())
        print()
    print()
    input('Press enter to quit.')
    os.system('clear')


##################
# Save user data #
##################

def how_long():
    print('Enter how long you would like the round to last in seconds.')
    print('Minimum is 30 seconds, max is 120.\n')
    print()
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
    print()
    new = input('>')
    print()
    if new.lower() == 'n':
        user = new_player()
        # user.add_deck(dicts.EOSDICT)
    elif new.lower() == 'y':
        user = load_player()
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
    print()
    player_name = input('>')
    print()
    return User(player_name)


def load_player():
    print("Who is playing? ")
    print()
    player_name = input('>')
    print()
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
        print()
    response = valifate_response(ans_list)
    if response == 0:
        return load_player()
    elif response == 1:
        user = new_player()

        # FIX DECK
        # user.add_deck(dicts.EOSDICT)
        return user

# @TODO: update comments and documentation
# @TODO: read csv and split entries into dictionary


if __name__ == '__main__':
    os.system('clear')
    games_list = ['Player Stats', 'Memory']
    player = get_player()
    session_cards = []
    # failsafe until player db is finished
    session_cards = ['go', 'order 66', 'address']
    game = choose_list(games_list)
    if game == 'Player Stats':
        print("No stats yet")
        input('Press enter to quit.')
        sys.exit()
        # return_stats(player, set(session_cards, deck))
    elif game == 'Memory':
        choice = choose_list(DECKLIST)
        deck = dicts.ALL_DECKS[choice]
        player.add_deck(deck)
        print(deck['__dict_name__'])
        game_cards, player = m.memory(player, deck)
        session_cards.extend(game_cards)
        return_stats(player, set(session_cards), deck)
        save_player(player)
