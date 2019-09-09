import json


with open("config.json", "r") as read_file:
    data = json.load(read_file)


subs = input()

for stanza in data:
    if subs in stanza.get('urls','empty'):
        print(stanza['title'], stanza['config file'])