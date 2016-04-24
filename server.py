import json
import os

from flask import Flask
from flask import render_template
from flask import request

import risk

app = Flask(__name__)


# Controllers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/form_submission")
def form_submission():
    return '{"data": {"plans": [{"name": "Aetna HMO", "min": 1000, "max": 10000, "avg": 6000},{"name": "Blue Shield PPO", "min": 2000, "max": 15000, "avg": 4500}]}}'


# Actual Routes

@app.route("/")
def root():
    return render_template('index.html')


@app.route("/index.html")
def index():
    return root()


@app.route("/form1.html")
def form1():
    return render_template('form1.html')


@app.route("/form2.html")
def form2():
    return render_template('form2.html')


@app.route("/plans.html")
def plans():
    return render_template('plans.html')


@app.route("/details.html")
def details():
    return render_template('details.html')


@app.route("/fetch_stats", methods=['POST'])
def login():
    '''
    Input should be:
    {
        'age': 20,
        'sex': 'M',
        'doctors': ['1235'],
        'specialists': ['12345'],
        'drugs': ['123']
    }
    '''
    data = request.form
    return json.dumps(risk.get_risk(
        data['age'],
        data['sex']))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # debug=True for autorestart
    app.run(host='0.0.0.0', port=port, debug=True)
