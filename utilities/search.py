# a command line untility to quickly search through the JSON output of
# config-to-json.py

import json
import sys

CONFIG_FILE = 'config.json'

with open(CONFIG_FILE, "r") as read_file:
    data = json.load(read_file)


try:
    subs = sys.argv[1]
except IndexError:
    print(f'Usage: python {sys.argv[0]} [ url ]')
    sys.exit(1)  # abort

search_results = list()

for stanza in data:
    if subs in stanza.get('urls', 'empty'):
        new_stanza = {key: stanza[key] for key in ['title', 'config_file']}
        search_results.append(new_stanza)

print(*search_results, sep="\n" if search_results else 'URL not found')
