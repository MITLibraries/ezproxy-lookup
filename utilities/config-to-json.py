
##################################################################################################################
#
# config-to-json.py
#
# usage: python config-to-json.py [full path to ezproxy config file]
#
# This script parses our ezproxy config.txt file into JSON to be used by
# our ezproxy-lookup app.
#
# This script returns a JSON formatted list of objects representing ezproxy database stanzas.
# Each stanza in the list has the following keys:
#   title: from the 'title' directive for the stanza
#   config_file: the filename of the config file containing the stanza, e.g. econtrol_config.txt
#   urls: an array of the URLs from the Host, Domain, and Url directives for the stanza. 
#       paths and url params are removed from URLs in case there may be sensitive information there.
#
# This script will try to parse the contents of "included" config files if it encounters an IncludeFile directive
#
###############################################################################################################

import re
import json
import sys
from pathlib import Path


try:
    ezproxy_base_config_path = Path(sys.argv[1])

except:
    print(f'Usage: python {sys.argv[0]} [ ezproxy config.txt file ]')
    sys.exit(1)  # abort


#regular expression for parsing stanzas. First capture group is for t(itle), h(ost), d(omain, or u(rl) keywords. second capture group is for the value for that keyword
regex = re.compile(r'^(t(?:itle)?|h(?:ost)?j?|d(?:omain)?j?|u(?:rl)?|includefile)\s(.*)$', re.I)


def parse_config(path_to_config):

    # a list to hold all of the stanzas in the config file
    stanzas = list()

    #a dict to hold the current stanza
    currentstanza = dict()

    with path_to_config.open() as f:
        for line in f:

            # if we don't find a directive we care about e.g. T(itle), H(ost), D(omain), U(rl), or includefile, 
            # move to the next line in the config file
            if regex.search(line):
            
                # the regex finds a directive
                directive = regex.search(line)
                                    
                #if includefile directive is encountered
                if directive.group(1).lower() == "includefile":
                    included_config = path_to_config.with_name(directive.group(2).strip()) 
                    
                    # An Includefile directive indicates we've reached the start of a new stanza. 
                    # if there is an existing current stanza append it to the list of stanzas
                    # Start a new current stanza.
                    
                    if currentstanza: 
                        stanzas.append(currentstanza.copy())
                        currentstanza = dict()    
                    #parse the contents of the included config file and return a list of stanzas
                    included_stanzas = parse_config(included_config)

                    #if the included config file contains stanzas add them to our list 
                    if included_stanzas: stanzas.extend(included_stanzas)
                    

                #if a title directive is encountered begin a new stanza
                elif directive.group(1).lower() in ["t","title"]:
            
                    # A title directive indicates we've reached the start of a new stanza. 
                    # if there is an existing current stanza append it to the list of stanzas
                    if currentstanza: stanzas.append(currentstanza.copy())
                    
                    #set the title 
                    currentstanza["title"] = directive.group(2)

                    #set the config file 
                    currentstanza["config_file"] = path_to_config.name

                    #initialize an empty list of URLs 
                    currentstanza["urls"] = list()

                # otherwise it is a url, host, or domain directive
                # regex removes anything after the Top Level Domain in case there is sensitive info in url params
                # add the url to the urls list in the current stanza            
                else:
                    matched_url = re.search(r'((?:https?:\/\/)?[a-z\d.-]+\.[a-z\d]{2,6})(?:[\/:?=@&#]{1}.+)?\/?$',directive.group(2), re.I)
                    if matched_url:
                        currentstanza["urls"].append(matched_url.group(1))
                
               

        #we reached the end of the file. add the last stanza to the list of stanzas        
        if currentstanza: stanzas.append(currentstanza.copy())    
    
        #return the list of stanzas
        return stanzas
        
all_stanzas = parse_config(ezproxy_base_config_path)
print(json.dumps(all_stanzas))

    