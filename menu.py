#!/usr/bin/python3


"""
This program serves as a hub for simple command line games.

# @TODO:
* [ ] - add ordered dict to printing dicts.ALL_DECKS
* [ ] - @TODO: update comments and documentation
* [ ] - edit eosdict definitions for length
* [ ] - format printing of definitions to fit to screen
* [ ] - add update_deck method to User class in case deckk changes

"""


# IMPORTS
import os
import sys
import pprint
import shelve
import dicts
import memory as m
import utils


def choose_deck():
    """Display options and return user deck choice."""
    deck_prompt = "What deck would you like to play?"
    choice = utils.choose_list(utils.DECKLIST, deck_prompt)
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
            return utils.User(player_name)


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
    response = utils.choose_list(ans_list, noname_prompt)
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
    game = utils.choose_list(games_list, game_prompt)
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
