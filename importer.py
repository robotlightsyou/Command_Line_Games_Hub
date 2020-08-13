#!/usr/bin/python3


#@TODO: use re module to censor defs nb ATBS chapter
#@TODO: accept command line args for __dict_name__


import re
import csv
import pprint


with open('eoslong.csv', 'r') as f:
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
    with open('dicts.py', 'a') as out:
        out.write('\n\nEOSDICT = {')
        for k,v in result.items():
            out.write(f"'{k}': '{v}',\n")
        out.write('}')
print('Done')
