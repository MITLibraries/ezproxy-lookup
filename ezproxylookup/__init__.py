from flask import Flask

app = Flask(__name__)

import ezproxylookup.views
import ezproxylookup.helpers
