# ezproxy-lookup
exproxy-lookup is a python flask application for checking whether
a given URL is configured for proxying in a set of [ezproxy](https://www.oclc.org/en/ezproxy.html) configuration files

It offers a simple web-interface and an API

## Why do we need this?
When troubleshooting ezproxy access to a particular resource it is important to understand if ezproxy is configured correctly.

Ezproxy-lookup gives staff a quick way to check a URL for a resource against ezproxy's configuration without having access to the actual config files.

There are some legacy perl scripts that perform a similar function. They use an undocumented xml-api that comes with ezproxy.

https://wikis.mit.edu/confluence/display/LIBPROXSERV/Proxy+lookup+scripts

## Things to Know
- Use [utilities/config_to_json.py](https://github.com/MITLibraries/ezproxy-lookup/blob/master/utilities/config_to_json.py) to parse the ezproxy config.txt file into JSON to be used by ezproxy-lookup. 
- [utilities/search.py](https://github.com/MITLibraries/ezproxy-lookup/blob/master/utilities/search.py) is a command line script to help with debugging the JSON output from config_to_json.py. (so you don't have to start up the whole flask app.)
- No authentication or authorization is required to use the web ui or API. [utilities/config-to-json.py](https://github.com/MITLibraries/ezproxy-lookup/blob/master/utilities/config-to-json.py) removes any sensitive information from our config files. 
- We are using a heroku deployment pipeline currently deploying master branch automatically to https://ezproxy-lookup-stage.herokuapp.com/
- If flask is run in development mode, it will look for the JSON file specified in the `DEV_CONFIG_JSON` environment variable, instead of trying to access the one in s3. 

## Required Environment Variables
- `AWS_ACCESS_KEY_ID` : for the ezproxy-lookup user (readonly)
- `AWS_SECRET_ACCESS_KEY` : for the ezproxy-lookup user (readonly)
- `AWS_BUCKET_NAME` : name of s3 bucket containing JSON created by [utilities/search.py](https://github.com/MITLibraries/ezproxy-lookup/blob/master/utilities/config_to_json.py)
- `DEV_CONFIG_JSON` : the path to a local JSON file (as created by [utilities/search.py](https://github.com/MITLibraries/ezproxy-lookup/blob/master/utilities/config_to_json.py) ) to use for development, in case you don't have access to the s3 bucket 


## API usage
- you can `POST` a `URL` with header set to `Accept: application/json` to get a JSON response
- example: `curl -d "url=jstor.org" -H "Accept: application/json" -X POST https://ezproxy-lookup-stage.herokuapp.com/`
