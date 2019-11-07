########################################
# config-to-json.py
#
# usage: python config-to-json.py [full path to ezproxy config file]
#
# This script parses our ezproxy config.txt file into JSON to be used by
# our ezproxy-lookup app.
#
# This script returns a JSON formatted list of objects representing ezproxy
# database stanzas.
# Each stanza in the list has the following keys:
#   title: from the 'title' directive for the stanza
#   config_file: the filename of the config file containing the stanza,
#        e.g. econtrol_config.txt
#   urls: an array of the URLs from the Host, Domain, and Url directives for
#       the stanza. paths and url params are removed from URLs in case there
#       may be sensitive information there.
#
# This script will try to parse the contents of "included" config files if it
# encounters an IncludeFile directive
########################################

import re
import sys
from pathlib import Path
import json


def main():
    try:
        with open(sys.argv[1]) as f:
            base_config_file = f.read()
        config_file_path = Path(sys.argv[1])

        # get included files from base file
        include_file_names = get_included_files(base_config_file)

        # add base config file name to list of file names
        config_files = include_file_names + [config_file_path.name]

        # get contents from each config file
        config_file_data = [
            {"config_file": file_name,
             "content": get_config_contents(config_file_path.with_name
                                            (file_name))}
            for file_name in config_files]

        # parse the data from each file
        results = []
        for data in config_file_data:
            if get_stanzas(data):
                results.extend(get_stanzas(data))
        print(json.dumps(results))
    except IndexError:
        print(
            f'''
please provide the full path to an ezproxy config file
Usage: python {sys.argv[0]} /path/to/ezproxy config
        ''')
        sys.exit(1)  # abort


# regular expression for parsing stanzas. First capture group is for t(itle),
# h(ost), d(omain, or u(rl) keywords. second capture group is for the value for
# that keyword
stanza_regex = re.compile(r"""^(t(?:itle)?|h(?:ost)?j?|d(?:omain)?j?|
u(?:rl)?)\s(.*)$""", re.I | re.X | re.MULTILINE)

# regular expression for matching url-like strings and removing paths
# and query string params
url_regex = re.compile(r"""
(                      # start capturing group for what we want
    (?:https?:\/\/)?   # in non-capturing group match protocol if there is one
    [a-z\d.-]+         # match everything up to the top level domain
    \.                 # match a '.'
    [a-z\d]{2,6}       # match the top level domain
)                      # end capturing group
(?:[\/:?=@&#]{1}.+)?   # in a non capturing group match paths or params
    \/?                # check for trailing slash
    $""", re.I | re.X)


def get_included_files(base_config_file_text):
    """ return a list of the file names from the includefile directives found
    in a config file """
    matches = re.findall(r"""^(includefile)\s(.*)$""", base_config_file_text,
                         re.I | re.X | re.M)
    included_files = [match[1].strip() for match in matches]
    return(included_files)


def get_config_contents(config_file_name):
    """ returns a list of strings from a config file

    returns '' if file cannot be opened

    config_file_name: the path of a config file

    """
    try:
        with open(config_file_name) as f:
            return(f.readlines())
    except IOError:
        return ''


def get_stanzas(config_data: str):
    """ returns a list of stanzas in a config file

        config_data: the contents of a config file as a string
    """
    # a list to hold all of the stanzas in the config file
    stanzas = []

    # a dict to hold the current stanza
    currentstanza = {}

    for line in config_data['content']:

        # if we don't find a directive we care about e.g. T(itle), H(ost),
        # D(omain), U(rl), or includefile,
        # move to the next line in the config file
        if stanza_regex.search(line):

            # the regex finds a directive
            directive = stanza_regex.search(line)

            # if a title directive is encountered begin a new stanza
            if directive.group(1).lower() in ["t", "title"]:

                # A title directive indicates we've reached the start of a
                # new stanza.
                # if there is an existing current stanza append it to the
                # list of stanzas
                if currentstanza:
                    stanzas.append(currentstanza)

                # set the title for a new stanza
                currentstanza = {
                    "title": directive.group(2),
                    "config_file": config_data['config_file'],
                    "urls": list()
                }

            # otherwise it is a url, host, or domain directive
            # strip out paths and query params from the url
            # add the url to the urls list in the current stanza
            else:
                matched_url = re.search(url_regex, directive.group(2))
                if matched_url:
                    currentstanza["urls"].append(matched_url.group(1))
    # we reached the end of the file. add the last stanza to the list
    # of stanzas
    if currentstanza:
        stanzas.append(currentstanza)
        return stanzas


if __name__ == "__main__":
    main()
