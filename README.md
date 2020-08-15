# Command Line Games Hub

## Update: 14 Aug 2020

Command Line Games Hub is a central player tracker for games. Presently
the only functioning game is Flash Cards, but more are in development. 
Ultimately the plan is to migrate to a Django driven web app.

### menu.py

Menu is the actual hub. When this program is run you will be presented
with the option to load a player or start a new save. Next you will be
asked which game you would like to play. After there may be some setup
screens before the game is started. At the conclusion of the session player stats for that
game will be displayed and the player's progress saved.

* To do - move Term to memory for cleanliness?
* To do - create seesion class to better track session attributes

### memory.py

The engine for the flash card game. Can be run from menu.py or called
independently. If run from menu player stats will be tracked and multiple
rounds can be played. If run directly from memory.py it will act as a
quick round.

* To do - print formatting on definitions
* To do - add more decks
        
### importer.py

Importer is a helper program that will try to import a dictionary into 
dicts.py from an external CSV. Currently the CSV must be one column, with 
the term at the start of the cell, followed by a ':', followed by the
definition. Importer will attempt to sterilize any mentions of term in
the definition, but it is a brute tool that will likely require manual
editing. 

### dicts.py

This is a reference document for the flash cards, and contains the actual
terms and definitions. You can manually add dictionaries or use importer.
Make sure to update ALL_DICTS if you do add a deck.

## Usage:

clone repository and run from command line using:
    
    python menu.py
    python memory.py
    
importer.py takes 3 command line arguments, the source file, the name of the
variable for your new dictionary, and the printed form of your dictionary's 
name:

    python importer.py /path/to/source.csv code_formatted_dict_name "Human Readable Dictionary Name"
    
## Requirements:

Uses fstrings so you will need as least python 3.6. All imported modules
part of standard library.
