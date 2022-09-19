from flask import Flask, render_template

app = Flask(__name__)


# @app.route('/index')
# def hello():
#     return render_template('index.html')


@app.route('/')
def mainRoute():
    return render_template('base.html')

# Use flask templates for logic, linking and overall tutorials
# https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application#step-4-using-conditionals-and-loops
# THEN build out backend, add frontend/then bootstrap and angular