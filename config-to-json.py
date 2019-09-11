import re
import json

#TODO: check for command line argument, or prompt for filename
main_config_file = "config.txt"


#regular expression for parsing stanzas. First capture group is for t(itle), h(ost), d(omain, or u(rl) keywords. second capture group is for the value for that keyword
regex = re.compile(r'^(t(?:itle)?|h(?:ost)?j?|d(?:omain)?j?|u(?:rl)?|includefile)\s(.*)$', re.I)


def parse_config(config_file):

    # a list to hold all of the stanzas in the config file
    stanzas = list()

    #a dict to hold the current stanza
    currentstanza = dict()

    with open(config_file) as f:
        for line in f:

            #we only care about T(itle), H(ost), D(omain), U(rl), or includefile lines
            if not regex.search(line): continue
            
            # the regex finds a directive
            directive = regex.search(line)
                                  
            #if includefile directive is encountered
            if directive.group(1).lower() == "includefile":
                included_config = directive.group(2).strip() 
                
                #we've reached the end of a stanza. append the current stanza (if there is one) to the list of stanzas
                if currentstanza: 
                    stanzas.append(currentstanza.copy())
                    currentstanza = dict()    
                #parse the contents of the included config file and return a list of stanzas
                included_stanzas = parse_config(included_config)

                #if the included config file contains stanzas add them to our list 
                if included_stanzas: stanzas.extend(included_stanzas)
                

            #if a title directive is encountered begin a new stanza
            elif directive.group(1).lower() in ["t","title"]:
        
                #if there is an existing current stanza append it to the list of stanzas
                if currentstanza: stanzas.append(currentstanza.copy())
                
                #set the title 
                currentstanza["title"] = directive.group(2)

                #set the config file 
                currentstanza["config_file"] = config_file

                #initialize an empty list of URLs 
                currentstanza["urls"] = list()

            # otherwise it is a url, host, or domain directive
            # add it to the urls list in the current stanza            
            else:
                matched_url = re.search(r'[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-zA-Z0-9]*\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?',directive.group(2))
                if matched_url:
                    currentstanza["urls"].append(directive.group(2))
                
               

        #we reached the end of the file. add the last stanza to the list of stanzas        
        if currentstanza: stanzas.append(currentstanza.copy())    
    
        #return the list of stanzas
        return stanzas
        
all_stanzas = parse_config(main_config_file)
print(json.dumps(all_stanzas))

    