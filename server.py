import os

from flask import Flask
from flask import render_template

app = Flask(__name__)

# Controllers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=port, debug=True)  # debug=True for autorestart
