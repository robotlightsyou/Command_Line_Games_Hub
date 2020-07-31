#!/usr/bin/python3

'''
This program is a command line text game that challenges the user on
their knowledge of ETC Eos terminology.

@TODOS:
* [ ] - weight answers for user comfort/difficulty
* [X] - completed - change ask_q to be numbers to avoid str coersion
  [ ] --> timer added, troubleshoot methods
* [ ] - add GUI - most likely web inteface
* [ ] - calling list() a lot when genrating answers, would be better for runtime
    to store all values at beginning?
* [ ] - add try block for input validation in ask_q()
* [ ] - add fake answer check to avoid repeats

* [X] - completed - change ask_q to be numbers to avoid str coersion
* [X] - completed - Object inheritance is failing, research how to make objects
sub-object(?) instances nb User.(variable).attribute
* [X] - completed - redefine to also print definition#
* [X] - completed - redfine so dictionary name is included in Term object
* [X] - completed - add method(s) to print stats
'''

import random
import time
import os
from pprint import pprint

# dictionary of {terms:defintions}
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

ANS_LIST = ['order 66', 'address', 'go']

#completed: redfine so dictionary name is included in Term object
class Term():
    def __init__(self, name, shared_dict, dict_name):
        self.name = name
        self .dict_name = dict_name
        self.defi = shared_dict[name]
        self.times_answeered = 0
        self.avg_time = 0
        self.cum_time = 0

    def update_time(self, start_time, end_time, answer):
        ans_time = end_time - start_time
        self.times_answeered += 1
        self.cum_time += ans_time
        self.avg_time = self.cum_time / self.times_answeered

    #completed: add method(s) to print stats
    def print_stats(self):
        print(self.__str__())
        print("Times answered: {}".format(self.times_answeered))
        print("Average Time: {}".format(self.avg_time))

    #completed: redefine to also print definition
    def __str__(self):
        return "{}: {}\n".format(self.name, self.defi)


class User():
    def __init__(self):
        self.cards = {}

    def add_deck(self, deck):
        for card in deck.keys():
            self.cards[card] = Term(card, EOSDICT, 'Eosdict')

def main():
    p = User()
    p.add_deck(EOSDICT)
    pprint(vars(p))
    print(p.cards["order 66"].__str__())
    p.cards["go"].print_stats()

#print("Who is playing? ")
#player = input('>')
# player = User(EOSDICT)
# memory(player)
# #memory()
# play_again(player)

# memory cards


def memory(user):
    past = []
    correct = 0
    timer = time.time()
    # while len(past) < len(EOSDICT):
    while len(past) < len(ANS_LIST):
        past = game(past, correct, user)
        if time.time() - 30 > timer:
            print("Time's up.")
            break

def game(answered, correct, user):
    time.sleep(1)
    os.system('clear')
    ans = get_ans(answered, EOSDICT)
    #print(f'answer = {ans}')
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
    '''
    answer = ""
    while True:
        # answer = pick random entry
        # answer = random.choice(list(EOSDICT.keys()))
        answer = random.choice(ANS_LIST)
        # compare answer against previous game answer
        if answer not in answered:
            break
    return answer

#@TODO: wrie check to ensure no repeats with eztra definitions
def get_anspad(answer):
    '''
    DOCSTRING: This function takes in the answer generated by get_ans(),
    pulls 3 additional definitions from EOSDICT, and compares them to
    confirm there are no duplicates.
    Returns a list "anspad" to be shuffled and printed
    '''
    # pick 3 additional defs that aren't answer
    anspad = []
    for _ in range(3):
        tmpans = EOSDICT[answer]
        while tmpans == EOSDICT[answer]:
            tmpans = random.choice(list(EOSDICT.values()))
        anspad.append(tmpans)
    return anspad

# shuffle answers


def shuffle(anspad, answer):
    '''
    DOCSTRING: This function takes in the list of defintions generated by
    get_anspad, shuffles them, and returns new list.
    '''
    anspad.append(EOSDICT[answer])
    random.shuffle(anspad)
    return anspad

# display question and answers


def ask_q(answer, anspad, user):
    '''
    DOCSTRING: This function takes in the answer and definitions, prints
    them, queries the user, and returns their the string definition
    the user chose.
    '''
    start_time = time.time()
    #print(f"What is the definition of {answer}?\n")
    print("What is the definition of {}?\n".format(answer))
    print("1) {}\n2) {}\n3) {}\n4) {}\n\n".format(
        anspad[0], anspad[1], anspad[2], anspad[3]))
#        f"1) {anspad[0]}\n2) {anspad[1]}\n3) {anspad[2]}\n4) {anspad[3]}\n\n")
    print("Answer: ")
    # add input verification
    response = int(input('>')) - 1
    end_time = time.time()
    user.update_time(start_time, end_time, answer)
    return anspad[response]

# receive and verify user input


def verify(answer, response):
    '''
    DOCSTRING: This function takes in the generated answer and the
    user's response, compares them, and prints the result. Returns
    True if correct, False if incorrect.
    '''
    result = EOSDICT[answer] == response
    if result:
        print("\n\n     Congrats! Nailed it!\n\n")
        return True
    else:
        print("\n\n     Sorry, incorrect.\n\n")
        return False


def play_again(user):
    '''
    DOCSTRING: This function asks the user if they want to play again
    if yes, restart memory, if no then exit.
    '''
    print("Would you like to play again?")
    print("Enter 'y' or 'n'")
    if input('>')[0].lower() != 'n':
        memory(user)


if __name__ == '__main__':
    main()


# log scores and track user

