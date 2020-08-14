# Command Line Games Hub

## Update: 14 Aug

Command Line Games Hub is a central player tracker for games. Presently
the only functioning game is Flash Cards, but more are in development. 
Ultimately the plan is to migrate to a Django driven web app.

### Menu.py

Menu is the actual hub. When this program is run you will be presented
with the option to load a player or start a new save. Next you will be
asked which game you would like to play. After there may be some setups
screens before the game is started.

* To do - move Term to memory for cleanliness?
* To do - create seesion class to better track session attributes

### Memory.py

The engine for the flash card game. Can be run from menu.py or called
independently. If run from menu player stats will be tracked and multiple
rounds can be played. If run directly from memory.py it will act as a
quick round.

* To do - weight questions based on user responses
* To do - print formatting on definitions
* To do - add more decks
        
### Importer.py

Importer is a helper program that will try to import a a dictionary into 
dicts.py from an external CSV. Currently the CSV must be one column, with 
the term at the start of the cell, followed by a ':', followed by the
definition. Importer will attempt to sterilize any mentions of term in
the definition, but it is a brute tool that will likely require manual
editing. After importing copy ALL_DICTS to the end of the file, and add
and entry for the new deck you just uploaded.

* To do - add 2 column option(one term, ne def)
* To do - insert new dict before ALL_DICTS
* To do - add new dict to ALL_DICTS

### Dicts.py

This is a reference document for the flash cards, and contains the actual
terms and definitions. You can manually add dictionaries or use importer.
Make sure to update ALL_DICTS if you do add a deck.

## Installation:

clone repository and run from command line using:
    
    python menu.py
    
## Requirements:

Uses fstrings so you will need as least python 3.6. All imported modules
part of standard library.
