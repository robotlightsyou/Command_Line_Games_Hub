# eos_flash_cards

##Update: 7 Aug

eoscard.py is now deprecated, I will be deleting it soon. The game currently works, 
you need menu.py, memory.py, and dicts.py all in the same folder, then run menu.py
and make your selection. Player Stats in the early menu is broken, but memory works, 
and printing player stats at the end of the game functions. You can add your own 
decks to the game by including a dictionary in dicts.py. You'll then need to 
add a key "__dict_name__" in the dictionary, as well as including the varible holding 
dictionary in the DICTS_LIST to make it callable from menu.py.

********

This is a basic command line program written to gain experience writing
python. 

Currently only a flash card game, but I have plans to expand some.

run from command line with

   ~~python3 ./eosflashcards ~~
   
    menu.py 
   
    #if shebang matches your interpreter, otherwise
   
    python3 ./meny.py
    
uses f strings so you need a newer python.

The game itself quizes the user on their knowledge of 
ETC Eos lighting terminology. Currently only utilizes a small
dictionary, but I hope to have the full Eos glossary fed in
soon.
