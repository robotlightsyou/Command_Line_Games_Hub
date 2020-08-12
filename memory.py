#!/usr/bin/python3

'''
DOCSTRING: This program runs a basic memory card game. If memory() is
    called for the menu it will take arguments, but if the program
    is runa s main the user will still be prompted for input.
    This docstring sucks, write better.
    Input:
        user: User, who is playing the game.
        deck: a {dictionary} of terms and definitions
        tlimit: integer - the time limit in seconds for the game
    Output:
        cards_played - a [list] of strings representing the card names
            from te most recent round
        user - an update User instance
'''
# @TODO: in return stats keep screen locked to top instead of following
# printing

import random
import time
import os
from pprint import pprint
import shelve
import menu as mu
import dicts


def memory(user, deck):
    '''
    DOCSTRING: This function is the main gameplay of the memory card
    game. It takes in a user, updates their stats each round, and
    a list of cards answered
    Input:
        User: user
    Output:
        List: game_cards
        User: the updated user object.
    '''
    # past is a list of all cards played in session
    past = []
    correct = 0
    tlimit = mu.how_long()
    timer = time.time()
    while len(past) < len(deck):
        past = one_round(past, correct, user, deck)
        # add 1 second to account for displaying results
        timer += 1
        if time.time() - tlimit > timer:
            print("Time's up.")
            print()
            break
    # play_again(user, deck)
    return past, user


def one_round(answered, correct, user, deck):
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
    ans = get_ans(answered, deck)
    defs = get_anspad(ans, deck)
    defs = shuffle(defs, ans, deck)
    respond = ask_q(ans, defs, user, deck)
    if verify(ans, respond, deck):
        answered.append(ans)
        correct += 1
        user.memory[deck['__dict_name__']][ans].update_correct()
    return answered


def get_ans(answered, deck):
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
        answer = random.choice(list(deck.keys()))
        # compare answer against previous game answer
        if answer not in answered:
            if answer != '__dict_name__':
                break
    return answer


def get_anspad(answer, deck):
    '''
    DOCSTRING: This function takes in the answer generated by get_ans(),
    pulls 3 additional definitions from deck, and compares them to
    confirm there are no duplicates.
    Returns a list "anspad" to be shuffled and printed
    Input:
        string: answered
    Output:
        list: anspad --> the 3 incorrect answers
    '''
    anspad = []
    while len(anspad) < 3:
        tmpans = deck[answer]
        while tmpans == deck[answer]:
            tmpans = random.choice(list(deck.values()))
        if tmpans not in anspad:
            if tmpans != deck['__dict_name__']:
                anspad.append(tmpans)
    return anspad


def shuffle(anspad, answer, deck):
    '''
    DOCSTRING: This function takes in the list of defintions generated by
    get_anspad, shuffles them, and returns new list.
    Input:
        list of strings: anspad
        string: answer
    '''
    anspad.append(deck[answer])
    random.shuffle(anspad)
    return anspad


def ask_q(answer, anspad, user, deck):
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
    print(f"What is the definition of {answer}?\n")
    print(
        f"1) {anspad[0]}\n2) {anspad[1]}\n3) {anspad[2]}\n4) {anspad[3]}\n\n")
    print("Answer: ")
    response = mu.valifate_response(anspad)
    end_time = time.time()
    user.memory[deck['__dict_name__']][answer].update_time(
        start_time, end_time)
    return anspad[response]


def verify(answer, response, deck):
    '''
    DOCSTRING: This function takes in the generated answer and the
    user's response, compares them, and prints the result. Returns
    True if correct, False if incorrect.
    Input:
        string: answer, response
    Output:
        boolean
    '''
    result = deck[answer] == response
    if result:
        print("\n\n     Congrats! Nailed it!\n\n")
        return True
    else:
        print("\n\n     Sorry, incorrect.\n\n")
        return False


def play_again(user, deck):
    '''
    DOCSTRING: This function asks the user if they want to play again
    if yes, restart memory, if no then exit.
    Input:
        User: user
    Output:
        No output, but can restart the game
    '''
    print(f"{user.name},\n\tWould you like to play again?")
    print("Enter 'y' or 'n'")
    if input('>')[0].lower() != 'n':
        memory(user, deck)


if __name__ == '__main__':
    user = mu.get_player()
    deck_prompt = "What deck would you like to play?"
    deck = mu.choose_list(mu.DECKLIST, deck_prompt)
    os.system('clear')
    memory(user, deck)
    play_again(user, deck)
