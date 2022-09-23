# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from PIL import Image # Imports PIL module 
import pytesseract # will convert the image to text string


# Folder to save upload photos to and file types 
UPLOAD_FOLDER = './UPLOADS'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Setting session type and key: https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# used to find ending type for file
def getExtension(inputFile):
    return '.' and inputFile.rsplit(".",1)[1].lower()


# will open the pic file in the uploads folder and convert to text
def openPic(filenameAndExtenstion):
    imageToOpen = Image.open(rf"./UPLOADS/{filenameAndExtenstion}") # sets url
    result = pytesseract.image_to_string(imageToOpen) 
    # write text in a text file and save it to source path   
    with open('./UPLOADS/outputText.txt',mode ='w') as file:     
        file.write(result)
        print(result)



## NEED DELETE function or to add it all on to an existing function

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@app.route('/')
def mainRouteFunc():
    return render_template('base.html')

# Uploading 
@app.route('/upload',methods=['GET', 'POST'])
def upload_file():
    uploaded_file = ''
    title = "Upload Image to Convert"
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            secureTheFile = secure_filename(file.filename)
            extensionType = getExtension(secureTheFile)

            # Filename below - Important for functions 
            filename = "Temp_Pic_Upload." + extensionType
                    #filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_file = secureTheFile
                    ##return redirect(url_for('download_file', name=filename))

            # function to convert to text
            openPic(filename)

            


    return render_template('upload.html', html_title = title, html_file = uploaded_file)


"""
@app.route('/upload',methods=['GET', 'POST'])
def upload_file():
    title = "Upload Image to Convert"
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))

    return render_template('upload.html', html_title = title)
"""


# @app.route('/index')
# def hello():
#     return render_template('index.html')


# Use flask templates for logic, linking and overall tutorials
# https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application#step-4-using-conditionals-and-loops
# THEN build out backend, add frontend/then bootstrap and angular