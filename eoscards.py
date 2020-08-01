#!/usr/bin/python3

'''
This program is a command line text game that challenges the user on
their knowledge of ETC Eos terminology.

@TODOS:
* [ ] - weight answers for user comfort/difficulty
* [ ] - add GUI - most likely web inteface
* [ ] - calling list() a lot when genrating answers, would be better for runtime
        to store all values at beginning?
* [ ] - add save file to track user through multiple sessions
        --> started - add file per user? add user folder?
* [ ] - add import deck functions that read a file/webpage and generates
        a new dictionary
* [ ] - create User attribute to track different dictionaries
* [ ] = why is return stats printing None? Why isn't it printing for all cards?
* [ ] - fix play again so that it goes more than one cycle deep
* [ ] - add function so user can choose duration of round
* [ ] - did adding input validation break times answered counter?
* [X] - add try block for input validation in ask_q()

* [X] - completed - change ask_q to be numbers to avoid str coersion
* [X] - completed - Object inheritance is failing, research how to make objects
        sub-object(?) instances nb User.(variable).attribute
* [X] - completed - redefine to also print definition
* [X] - completed - redfine so dictionary name is included in Term object
* [X] - completed - add method(s) to print stats
* [X] - add fake answer check to avoid repeats
* [X} - fix name prompt
* [X] - completed - change ask_q to be numbers to avoid str coersion
  [X] --> timer added, troubleshoot methods
'''

import random
import time
import os
from pprint import pprint
import shelve

# dictionary of {terms:defintion}
EOSDICT = {'go': 'execute a cue',
           'stop': 'pause a cue',
           'back': 'restore previous cue',
           'address': 'the digital location of an instrument',
           'query': 'grep patch',
           'snapshot': 'a preset for screen layouts',
           'submaster': 'not a fader',
           'fader': 'a playback for cuelists and other record targets',
           'load': 'prepare a cue in the Go button for next keypress',
           'palette': 'a recorded data object specific to a parameter type',
           'preset': 'a non specific data object, may contain palettes',
           'order 66': 'shutdown macro',
           'macro': 'recorded commands replayed on a single keypress'}

# debug option, replace most instances with EOSDICT
ANS_LIST = ['order 66', 'address', 'go']


class Term():
    def __init__(self, name, shared_dict, dict_name):
        self.name = name
        self .dict_name = dict_name
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
        print("Average Time: {:.2f}".format(self.avg_time))

    def __str__(self):
        return "'{}': {}".format(self.name, self.defi)


class User():
    def __init__(self, name):
        self.name = name
        self.cards = {}

    # rewrite so any deck name can be added
    def add_deck(self, deck):
        for card in deck.keys():
            self.cards[card] = Term(card, EOSDICT, 'Eosdict')


def main():
    print("Who is playing? ")
    player_name = input('>')
    player = User(player_name)
    # rewrite for multiple decks
    player.add_deck(EOSDICT)
    # pprint(vars(player))
    #print(player.cards["order 66"].__str__())
    game_cards = []
    game_cards.extend(memory(player))
    play_again(player)
    return_stats(player, set(game_cards))

# @TODO: add function so user can choose duration of round


def memory(user):
    '''
    DOCSTRING: This function is the main gameplay of the memory card
    game. It takes in a user, updates their stats each round, and
    a list of cards answered
    Input:
        User: user
    Output:
        List: game_cards
    '''
    # past is a list of all cards played in session
    past = []
    correct = 0
    timer = time.time()

    # rewrite to allow multiple decks
    # while len(past) < len(EOSDICT):
    while len(past) < len(ANS_LIST):  # remove after debugging
        past = one_round(past, correct, user)
        if time.time() - 30 > timer:
            print("Time's up.")
            break
    return past


def one_round(answered, correct, user):
    '''
    DOCSTRING: This function draws a card from the game deck, selects filler
    answers for multiple choice, queries the user, verifies the answer, updates
    the user stats, and returns an updated deck. If user is correct card is 
    removed from the draw deck, if incorrect card may appear again in round.
    input:
        answered: a list of terms already correctly answered in game
        correct: an integer representing total correct in game
        user: the profile to receive stats update
    output:
        answered: a list of correctly answered terms in this individual game.
    '''
    time.sleep(1)
    os.system('clear')
    ans = get_ans(answered, EOSDICT)
    # print(f'answer = {ans}')  #why did fstrings stop working?
    defs = get_anspad(ans)
    defs = shuffle(defs, ans)
    respond = ask_q(ans, defs, user)
    if verify(ans, respond):
        answered.append(ans)
        correct += 1
    return answered


def get_ans(answered, EOSDICT):
    '''
    DOCSTRING: This function takes in a list answered and a dictionaey
    EOSDICT. It selects a random entry from the dictionary and compares
    against the previous answers in the answered list.
    Input:
        list: answered to ensure no repeats
        dict: deck name, currently hard coded to EOSDICT
    Output:
        string: answer
    '''
    answer = ""
    while True:
        # answer = pick random entry
        # answer = random.choice(list(EOSDICT.keys()))
        answer = random.choice(ANS_LIST)  # remove after debugging
        # compare answer against previous game answer
        if answer not in answered:
            break
    return answer


def get_anspad(answer):
    '''
    DOCSTRING: This function takes in the answer generated by get_ans(),
    pulls 3 additional definitions from EOSDICT, and compares them to
    confirm there are no duplicates.
    Returns a list "anspad" to be shuffled and printed
    Input:
        string: answered
    Output:
        list: anspad --> the 3 incorrect answers
    '''
    # pick 3 additional defs that aren't answer
    anspad = []
    while len(anspad) < 3:
        tmpans = EOSDICT[answer]
        while tmpans == EOSDICT[answer]:
            tmpans = random.choice(list(EOSDICT.values()))
        if tmpans not in anspad:
            anspad.append(tmpans)
        # else:
        #    continue
    return anspad


def shuffle(anspad, answer):
    '''
    DOCSTRING: This function takes in the list of defintions generated by
    get_anspad, shuffles them, and returns new list.
    Input:
        list of strings: anspad
        string: answer
    '''
    anspad.append(EOSDICT[answer])
    random.shuffle(anspad)
    return anspad

# ask and answer an individual card


def ask_q(answer, anspad, user):
    '''
    DOCSTRING: This function takes in the answer and definitions, prints
    them, queries the user, and returns their the string definition
    the user chose.
    Input:
        string: answer
        list of strings: andpad
        User: user
    Output:
        string: anspad[response]
    '''
    start_time = time.time()
    #print(f"What is the definition of {answer}?\n")
    print("What is the definition of {}?\n".format(answer))
    print("1) {}\n2) {}\n3) {}\n4) {}\n\n".format(
        anspad[0], anspad[1], anspad[2], anspad[3]))
#        f"1) {anspad[0]}\n2) {anspad[1]}\n3) {anspad[2]}\n4) {anspad[3]}\n\n")
    print("Answer: ")
    # add input verification
    response = valifate_response()
    end_time = time.time()
    user.cards[answer].update_time(start_time, end_time)
    return anspad[response]


def valifate_response():
    '''
    DOCSTRING: This function actually gets the user's response and
    tests that it is one of the valid options
    Input:
    Output:
        integer: response
    '''
    response = -1
    while response not in [0, 1, 2, 3]:
        try:
            response = int(input('>')) - 1
        except ValueError:
            print("Please emter a valid response")
    # while response not in [1, 2, 3, 4]:
    if response not in [1, 2, 3, 0]:
        print("Please emter a valid response")
        #response = input('>')
        response = valifate_response()
    return response


# receive and verify user input


def verify(answer, response):
    '''
    DOCSTRING: This function takes in the generated answer and the
    user's response, compares them, and prints the result. Returns
    True if correct, False if incorrect.
    Input:
        string: answer, response
    Output:
        boolean
    '''
    result = EOSDICT[answer] == response
    if result:
        print("\n\n     Congrats! Nailed it!\n\n")
        return True
    else:
        print("\n\n     Sorry, incorrect.\n\n")
        return False

# fix non-looping issue for multiple game(in main?)


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
        memory(user)


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
        print(user.cards[card].print_stats())
        print()

###############
# Save user data
###############
# @TODO: use shelve to open .db file


def save_session(user):
    d = shelve.open("myfile.db")
    d[user.name] = user
    d.close

# @TODO: function to load user
# @TODO: user login? covered by asking user name and loading from there?
# @TODO: update comments and documentation
# @TODO: read csv and split entries into dictionary


if __name__ == '__main__':
    main()


# log scores and track user
