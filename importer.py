#!/usr/bin/python3

import csv
import pprint

with open('eoslong.csv', 'r') as f:
    reader = csv.reader(f)
    result = {}
    for row in reader:
        try:
            k,v = row[0].split(':', 1)
            #delete leading white space from definition
            for char in v:
                if char == ' ':
                    v = v[1:]
                else:
                    break
            v = v.replace('\n', ' ')
            result[k] = v
        except:
            pass
    # pprint.pprint(result)
    with open('dicts.py', 'a') as out:
        out.write('\n\nEOSDICT = {')
        for k,v in result.items():
            out.write(f"'{k}': '{v}',\n")
        out.write('}')
print('Done')
