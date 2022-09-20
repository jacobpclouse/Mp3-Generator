import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# from flask import Flask, render_template

app = Flask(__name__)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@app.route('/')
def mainRouteFunc():
    return render_template('base.html')

@app.route('/upload')
def uploadRouteFunc():
    title = "Upload Image to Convert"
    return render_template('upload.html', html_title = title)


# @app.route('/index')
# def hello():
#     return render_template('index.html')


# Use flask templates for logic, linking and overall tutorials
# https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application#step-4-using-conditionals-and-loops
# THEN build out backend, add frontend/then bootstrap and angular