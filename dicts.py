#!/usr/bin/python3
'''
DOCSTRING: This file is for storing python dictionaries with terms and
    definitions for the Memory Cards game. Input must be in the format of
    EOSDICT, and an entry must be manually added to DICTS_DICT in order
    new deck to be displayed.
'''


TESTDECK = {'go': 'execute a cue',
            'address': 'the digital location of an instrument',
            'submaster': 'not a fader',
            'fader': 'a playback for cuelists and other record targets',
            'order 66': 'shutdown macro',
            '__dict_name__': 'Sample Deck'}

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
           'macro': 'recorded commands replayed on a single keypress',
           '__dict_name__': 'Eos Terms'}

ALL_DECKS = {EOSDICT['__dict_name__']: EOSDICT,
             TESTDECK['__dict_name__']: TESTDECK}
# ALL_DECKS = {'Eos Terms': EOSDICT, 'Sample Deck': TESTDECK}
