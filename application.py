from flask import Flask, request, jsonify, render_template, url_for, redirect
import requests
import os
import requests
import json
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

#flask command does this on its own. we need to do it explicity for gunicorn
load_dotenv('.env')

with open("config.json", "r") as read_file:
    data = json.load(read_file)

app = Flask(__name__)

@app.route("/", methods=['POST'])
def index_post():
        # check for form data
        if 'url' in request.form:
            search_results = list()
            search_term = request.form['url']
            for stanza in data:
                if search_term in stanza.get('urls','empty'):
                    
                    #remove urls from stanza and add to search results
                    new_stanza = { key: stanza[key] for key in ['title', 'config file']}
                    search_results.append(new_stanza)
            if request.headers['Accept'] == "application/json": 
                return jsonify({"search_term" : search_term, "search_results" : search_results})
            else: 
                return render_template('index.html', search_term = search_term, response = search_results)
        
        return redirect(url_for('index_get'))
    
@app.route("/", methods=['GET'])
def index_get():
    return render_template('index.html')
