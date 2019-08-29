import json


with open("ezproxy_config.json", "r") as read_file:
    data = json.load(read_file)


subs = input()


for config_file, stanzas in data.items():
    for stanza in stanzas:
        if subs in stanza['urls']:
            print(config_file)