from flask import request, jsonify, render_template, url_for, redirect
from ezproxylookup import app
from ezproxylookup.helpers import get_json_file


@app.route("/", methods=['POST'])
def index_post():
    # check for form data
    search_term = request.form.get('url')
    if search_term:
        data = get_json_file()
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
    data = get_json_file()
    # return list of stanzas where config_file = "econtrol_config.txt"
    result = [stanza for stanza in data if "econtrol_config"
              in stanza['config_file']]
    return render_template(
        'index.html',
        search_term='all econtrol resources',
        response=result
        )
