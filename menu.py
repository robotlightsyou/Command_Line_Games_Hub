#!/usr/bin/python3


"""
This program serves as a hub for simple command line games.

# @TODO:
* [ ] - add ordered dict to printing dicts.ALL_DECKS
* [ ] - @TODO: update comments and documentation
* [ ] - edit eosdict definitions for length
* [ ] - format printing of definitions to fit to screen
* [ ] - add update_deck method to User class in case deckk changes

* [X] - fix anser/anspad selection so it ignores __dict_name__
* [X] - fix return_stats shows times_correct, update methods
* [X] - clean up preint formatting
* [X] - fix add_deck to check if deck exists
* [X] - play_again--> skipping straight to displaying stats, in memory, not menu
* [X]  - validate new player doesn't exist
* [X] - rewrite choose list to accept question phrase
* [X] - rewrite no_name() to use updated choose_list
* [X] - how to fix recursive return_stats issue?
* [X] - fix play_again so it goes more than 1 deep
* [X] - --> confirm returning user stas correctly
* [X] - @TODO: read csv and split entries into dictionary
* [X] - function to calculate total length of definitions in anspad for wighting
* [X] - why is return_stats printing none?
* [X] - weight terms towards problem cards

"""


# IMPORTS
import os
import sys
import pprint
import shelve
import dicts
import memory as m


# CONSTANTS
DECKSDICT = dicts.ALL_DECKS
DECKLIST = list(DECKSDICT.keys())


# CLASSES
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


# GAME SETUP
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


def how_long():
    """
    Set the time limit on the individual rounds of the game.

    Output:
    time -- integer number of seconds for the round to last.
    """
    # os.system('clear')
    print('Enter how long you would like the round to last in seconds.')
    print('Minimum is 30 seconds, max is 120.\n')
    time = input(">")
    print()
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


def choose_deck():
    """Display options and return user deck choice."""
    deck_prompt = "What deck would you like to play?"
    choice = choose_list(DECKLIST, deck_prompt)
    deck = dicts.ALL_DECKS[choice]
    os.system('clear')
    return deck


def play_memory(player, session_cards, deck):
    game_cards, player = m.memory(player, deck)
    session_cards.extend(game_cards)
    play_again(player, session_cards, deck)


# PLAYER SETUP
def get_player():
    """
    Direct player to new_player() or load_player().

    Output:
    user - the User instance of the player.
    """
    os.system('clear')
    print("Are you a returning player?\n[y/n]\n")
    new = input('>')
    print()
    if new.lower() == 'n':
        user = new_player()
    elif new.lower() == 'y':
        user = load_player()
    else:
        print("Please enter 'y' or 'n'")
        return get_player()
    return user


def new_player():
    """
    Get player name and confirm not already in loadfile.

    Output:
    user - the new User object created for the player.
    """
    print("Who is playing? \n")
    player_name = input('>')
    print()
    with shelve.open('myfile') as loadfile:
        try:
            ################
            ##  FIX THIS  ##
            ################
            if loadfile[player_name] == None:
                pass  # return User(player_name)
            else:
                print("I already have a player with that name.")
                print("Please try a different name:\n")
                return new_player()
        except KeyError:
            return User(player_name)


def load_player():
    """
    Load a USer instance from loadfile.

    Output:
    player_name -- string input from player
    """
    print("Who is playing? \n")
    player_name = input('>')
    print()
    with shelve.open('myfile') as loadfile:
        try:
            user = loadfile[player_name]
        except KeyError:
            return no_name()
    return user


def no_name():
    """
    Exception handler when load fails because User not found.

    Output:
    User: user, if new selected. Else load_player()
    """
    noname_prompt = "Sorry, I can't find that file. Would you like to:"
    ans_list = ["Try a different name", "Start a new save"]
    response = choose_list(ans_list, noname_prompt)
    if response == ans_list[0]:
        return load_player()
    elif response == ans_list[1]:
        user = new_player()
        return user


def save_player(user):
    """
    Update savefile or create new user entry.

    Input:
    user - the User instance for the player from this session.
    Output:
    no return but writes to file.
    """
    with shelve.open('myfile') as savefile:
        savefile[user.name] = user


# POST GAME

# @TODO: pretty print this so user doesn't have to scroll back to top.


def return_stats(user, recent_words, deck):
    """
    DOCSTRING: This function takes in a user and a list of session
    words and prints that users stats with those cards
    Input:
        User: user
        list of strings: recent_words
        dictionary: deck - the dictionary being tested
    Output:
        No output, prints to screen
    """
    os.system('clear')
    print(f"{user.name},")
    print("    In the last session you answered the following cards,")
    print("here's your stats for them:\n")
    for card in recent_words:
        user.memory[deck['__dict_name__']][card].print_stats()
        print()
    print()
    input('                                        Press enter to quit.')
    os.system('clear')


def play_again(user, session_cards, deck):
    """
    Ask user to play again, then restart or quit.

    Input:
    user -- the User instance for current player.
    """
    print(f"{user.name},\n\tWould you like to play again?")
    print("Enter 'y' or 'n'\n")
    if input('>')[0].lower() != 'n':
        print()
        play_memory(user, session_cards, deck)


if __name__ == '__main__':
    os.system('clear')
    player = get_player()
    games_list = ['Player Stats', 'Memory']
    game_prompt = "What game would you like to play?"
    game = choose_list(games_list, game_prompt)
    ################
    ##  Fix this  ##
    ################
    if game == 'Player Stats':
        print("No stats yet")
        input('Press enter to quit.')
        sys.exit()
    elif game == 'Memory':
        session_cards = []
        deck = choose_deck()
        player.add_deck(deck)
        play_memory(player, session_cards, deck)
        return_stats(player, set(session_cards), deck)
    save_player(player)
