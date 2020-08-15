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


with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f)
    result = {}
    for row in reader:
        try:
            k,v = row[0].split(':', 1)
            #delete leading white space from definition
        except:
            pass
        for char in v:
            if char == ' ':
                v = v[1:]
            else:
                break
        v = v.replace('\n', ' ')
        v = v.replace("'", "\\'")
        occurances = re.findall(k,v, re.IGNORECASE)
        for occurance in occurances:
            v = v.replace(occurance, "*****")
        result[k] = v
    with open('dicts.py', 'r') as infile:
        lines = infile.readlines()
    for index, line in enumerate(lines):
        if line.startswith("ALL_DICTS"):
            break
    lines.insert(index - 3, "}")
    for k,v in result.items():
        lines.insert(index - 3, f"'{k}': '{result[k]}',\n")
    lines.insert(index - 3, "'__dict_name__': '{}',\n".format(sys.argv[3]))
    lines.insert(index - 3, f"{sys.argv[2]} = {{")
    lines.insert(index - 3, "\n\n")
    with open('dicts.py', 'w') as outfile:
        contents = outfile.writelines(lines)
print('Done')
