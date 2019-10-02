from flask import Flask, request, jsonify, render_template, url_for, redirect
import json
from dotenv import load_dotenv
import boto3
import os


#flask command does this on its own. we need to do it explicity for gunicorn
load_dotenv('.env')



app = Flask(__name__)

CONFIG_FILE = 'config.json'

#use a local config.json file for development
if app.env == "development":
    with open(CONFIG_FILE, "r") as read_file:
        data = json.load(read_file)
else:
#get config.json from s3 bucket
    s3 = boto3.resource('s3')
    obj = s3.Object('ezproxy-lookup-stage', CONFIG_FILE)
    body = obj.get()['Body'].read()
    data = json.loads(body)

@app.route("/", methods=['POST'])
def index_post():
        # check for form data
        search_term = request.form.get('url')
        if search_term:
            # return any stanzas containing matching urls      
            search_results = [stanza for stanza in data if search_term in stanza['urls']]
            if request.headers['Accept'] == "application/json": 
                return jsonify(search_term = search_term, response = search_results)
            else: 
                return render_template('index.html', search_term = search_term, response = search_results)
        return redirect(url_for('index_get'))
    
@app.route("/", methods=['GET'])
def index_get():
    return render_template('index.html')

@app.route("/econtrol")
def econtrol():
    #return list of stanzas where config_file = "econtrol_config.txt"
    result = [stanza for stanza in data if "econtrol_config" in stanza['config_file']]
    return render_template('index.html', search_term = 'all econtrol resources', response=result)


