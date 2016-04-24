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


@app.route("/fetch_stats", methods=['GET'])
def fetch_stats():
    '''
    GET /fetch_stats
    Returns percentages of hitting a health condition.

    Input should be:
        'age': 20,
        'sex': 'M',
    '''
    data = request.args
    return json.dumps(risk.get_risk(
        data['age'],
        data['sex']))


@app.route("/fetch_plan", methods=['GET'])
def fetch_plan():
    '''
    GET /fetch_plan
    Returns stats depicting how well a given plan will cover multiple health
    conditions.

    Input should be:
        'age': 20,
        'plan_id': '2938fawf' // StandardComponentId column in MySQL tables.
    '''
    return json.dumps(
        risk.get_plan(request.args['plan_id'], request.args['age']))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # debug=True for autorestart
    app.run(host='0.0.0.0', port=port, debug=True)
