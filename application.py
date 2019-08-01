from flask import Flask, request, jsonify, render_template
import requests
import os
import requests
import json
import dotenv
import xml.etree.ElementTree as ET

# Check for environment variables
if not os.getenv("PROXY_URL_PASSWORD"):
    raise RuntimeError("PROXY_URL_PASSWORD is not set")

# password for ezproxy API
PASSWORD = os.environ.get('PROXY_URL_PASSWORD')
# exprozy API endpoint
EZPROXY_API = "http://libproxy.mit.edu/proxy_url"

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check for post data
        if request.form['url']:
            # build xml request to send to ezproxy
            # TODO: handle multiple urls
            root = ET.Element("proxy_url_request", password=PASSWORD)
            urls_elem = ET.SubElement(root, "urls")
            url_elem = ET.SubElement(urls_elem, "url")
            url_elem.text = request.form['url']
            xml_request_data = ET.tostring(root)
            # send the xml request to ezproxy's API
            try:
                print(xml_request_data)
                response = requests.post(EZPROXY_API, data=xml_request_data)
                response.raise_for_status()
                proxy_doc = ET.fromstring(response.content)
                print(ET.dump(proxy_doc))
                return_dict = {}
                for u in proxy_doc.findall('./proxy_urls/url'):
                    orig_url = u.text
                    return_dict[orig_url] = u.get('proxy')
                # handle HTTP Accept headers
                if request.headers['Accept'] == "application/json" :
                    return jsonify(return_dict)
                return render_template('index.html', response = return_dict)
            except requests.exceptions.HTTPError as err:
                return render_template('index.html', error = err)
        
    return render_template('index.html')


    