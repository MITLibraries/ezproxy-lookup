import json


with open("ezproxy_config.json", "r") as read_file:
    data = json.load(read_file)


subs = input()

for stanza in data:
    if subs in stanza.get('urls','empty'):
        print(json.dumps(stanza))