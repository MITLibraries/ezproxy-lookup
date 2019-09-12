from flask import Flask, request, jsonify, render_template, url_for, redirect
import json
from dotenv import load_dotenv
import boto3


#flask command does this on its own. we need to do it explicity for gunicorn
load_dotenv('.env')

#get config.json from s3 bucket
s3 = boto3.resource('s3')
obj = s3.Object('ezproxy-lookup-stage','config.json')
body = obj.get()['Body'].read()
data = json.loads(body)

app = Flask(__name__)

@app.route("/", methods=['POST'])
def index_post():
        # check for form data
        url = request.form.get('url')
        if url:
            print(request.form['url'])
            search_results = list()
            search_term = request.form['url']
            for stanza in data:
                if search_term in stanza.get('urls','empty'):
                    
                    #remove urls from stanza and add to search results
                    new_stanza = { key: stanza[key] for key in ['title', 'config_file']}
                    search_results.append(new_stanza)
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
    result = list(filter(lambda stanza: ("econtrol_config" in stanza['config_file']), data))
    return render_template('index.html', search_term = 'all econtrol resources', response=result)