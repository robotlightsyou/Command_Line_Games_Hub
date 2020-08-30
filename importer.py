#!/usr/bin/python3

'''
DOCSTRING: This program loads dictionaries into dicts.py. Reads one
    column CSVs where the start of the cell is the term, then there
    is a colon(:), and the rest of the cell is the definition.
Input: program takes 3 command line arguments, 1) the source file
    for the definitions. 2) the name of the variable for the dictionary 
    in dicts.py. 3) the pretty print name of the dictionary, put in quotes
    if more than one word.
Output: No output, but appends to dicts.py
'''


import re
import csv
import pprint
import sys

def importer():
    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f)
        result = {}

        for row in reader:
            try:
                k,v = row[0].split(':', 1)
            except:
                pass

            #delete leading white space from definition
            for char in v:
                if char == ' ':
                    v = v[1:]
                else:
                    break

            #format text to avoid print errors
            #remove CSV line breaks from text
            v = v.replace('\n', ' ')
            #escape internal quotes for less manual editing
            v = v.replace("'", "\\'")
            #if term in definition, sterilize
            occurances = re.findall(k,v, re.IGNORECASE)
            for occurance in occurances:
                v = v.replace(occurance, "*****")
            #finall add term to dictionary
            result[k] = v

        #read all of dicts.py to have clean copy to edit into
        with open('dicts.py', 'r') as infile:
            lines = infile.readlines()
        #find the line with ALL_DICTS to insert before
        for index, line in enumerate(lines):
            if line.startswith("#PASTE"):
                break
        ## add new dict to ALL_DICTS
        lines.insert(index + 3, f"             {sys.argv[2]}['__dict_name__']: {sys.argv[2]},\n")
        # add new terms before ALL_DICTS to preserve functionality
        lines.insert(index - 1, "\n\n")
        lines.insert(index - 1, "}")
        # add individual terms
        for k,v in result.items():
            lines.insert(index - 1, f"'{k}': '{result[k]}',\n")
        # add __dict_name__ key to new dict for memory.py
        lines.insert(index - 1, "'__dict_name__': '{}',\n".format(sys.argv[3]))
        lines.insert(index - 1, f"{sys.argv[2]} = {{")
        lines.insert(index - 1, "\n")

        #overwrite dicts.py with new dictionary inluded
        with open('dicts.py', 'w') as outfile:
            contents = outfile.writelines(lines)

    print('Done')

if __name__ == '__main__':
    importer()

