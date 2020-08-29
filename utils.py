#!/usr/bin/python3

import pprint
import os


class Term():
    """
    The actual flash cards, unique to User instance.

    Input:
    name - string name of memory card
    deck - the dictionary/deck containing this card
    """

    def __init__(self, name, deck):
        self.name = name
        self .dict_name = deck['__dict_name__']
        self.defi = deck[name]
        self.times_answeered = 0
        self.times_correct = 0
        self.avg_time = 0
        self.cum_time = 0
        self.weight = 1_000

    def update_time(self, start_time, end_time):
        """
        Updates User stats for Term after each time Term is asked.

        Input:
        start_time -- inetger - when the question was asked.
        end_time -- integer - when the answer was given.
        Output:
        No return but does modify User stats
        """
        ans_time = end_time - start_time
        self.times_answeered += 1
        self.cum_time += ans_time
        self.avg_time = self.cum_time / self.times_answeered

    # should be using setattr()?

    def update_correct(self):
        self.times_correct += 1

    def print_stats(self):
        pprint.pprint(self.__str__())
        print(f"Times answered: {self.times_answeered}")
        print(f"Times correct: {self.times_correct}")
        print(f"Average Time: {self.avg_time:.1f}")
        print(f"Weight: {self.weight}")

    def update_weight(self, integer):
        self.weight = integer / self.avg_time
        # self.divtime = integer / self.avg_time
        # self.divlen = self.avg_time/ integer
        # self.multtime = integer * self.avg_time
        # print(f"div time = {self.divtime}\ndiv len = {self.divlen}")
        # print(f"multtime = {self.multtime}")
        # input('press enter')

    def __str__(self):
        return f"'{self.name}': {self.defi}"


class User():
    """
    Store stats about games played and player information.

    Input:
    string -- the name used to reference player, a User object.
    """

    def __init__(self, name):
        self.name = name
        #create a dictionary for each game to store User history
        self.memory = {}
        self.memory_decks = []

    def add_deck(self, deck):
        """
        Create Term objects in the player.memory dictionary.

        Input:
        deck - dictionary: chosen from dicts.py
        """
        name = deck['__dict_name__']
        # first check if player has previously played deck
        if name not in self.memory_decks:
            self.memory_decks.append(name)
            self.memory[name] = {}
            for card in deck.keys():
                self.memory[name][card] = Term(card, deck)


def valifate_response(ans_list):
    """
    Take in user response and test it is valid.

    Input:
    ans_list -- the options printed by choose_list()
    Output:
    response -- an integer
    """
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


def choose_list(options, prompt):
    """
    Display options and return player choice.

    Input:
    options -- the list to be printed
    Output:
    object -- the list item at the index of the player's choice, type
    depends on input.
    """
    os.system('clear')
    print(prompt)
    for index, value in enumerate(options):
        print(f'{index + 1}) {value}')
    print()
    response = valifate_response(options)
    print()
    return options[response]
