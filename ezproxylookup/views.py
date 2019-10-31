import os
from flask import request, jsonify, render_template, url_for, redirect
import json
import boto3
from ezproxylookup import app


# get config.json from s3 bucket.
def get_file():
    s3 = boto3.resource('s3')
    obj = s3.Object(os.getenv('AWS_BUCKET_NAME'), 'config.json')
    body = obj.get()['Body'].read()
    data = json.loads(body)
    return data


@app.route("/", methods=['POST'])
def index_post():
    # check for form data
    search_term = request.form.get('url')
    if search_term:
        data = get_file()
        # return any stanzas containing matching urls
        search_results = [
            stanza for stanza in data if search_term in stanza['urls']]
        if request.headers['Accept'] == "application/json":
            return jsonify(search_term=search_term, response=search_results)
        else:
            return render_template(
                'index.html',
                search_term=search_term,
                response=search_results
                )
    return redirect(url_for('index_get'))


@app.route("/", methods=['GET'])
def index_get():
    return render_template('index.html')


@app.route("/econtrol")
def econtrol():
    data = get_file()
    # return list of stanzas where config_file = "econtrol_config.txt"
    result = [stanza for stanza in data if "econtrol_config"
              in stanza['config_file']]
    return render_template(
        'index.html',
        search_term='all econtrol resources',
        response=result
        )
