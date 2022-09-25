# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import os
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image # Imports PIL module 
import pytesseract # will convert the image to text string
from gtts import gTTS # Import module for text to speech conversion
from cryptography.fernet import Fernet # will be used for encrypting output


# Folder to save upload photos to and file types 
UPLOAD_FOLDER = './UPLOADS'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Folder to save files that I will be sending to the user
OUTBOUND_FOLDER = './OUTBOUND'



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Setting session type and key: https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# used to find ending type for file AND checking to make sure that it is an allowed type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# used to find ending type for file only (for creating temp pic in UPLOADS)
def getExtension(inputFile):
    return '.' and inputFile.rsplit(".",1)[1].lower()



# will open the pic file in the uploads folder, convert to text, then convert text to mp3
def openPic(filenameAndExtenstion):

    """ This portion Converts Img to Text """
    imageToOpen = Image.open(rf"./UPLOADS/{filenameAndExtenstion}") # sets url
    result = pytesseract.image_to_string(imageToOpen) 
    # write text in a text file and save it to source path   
    with open('./UPLOADS/outputText.txt',mode ='w') as file:     
        file.write(result)
        print(result)


    """ This portion Converts Text to Mp3 """
    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine, slow=False means converted audio will have high speed
    myobj = gTTS(text=result, lang=language, slow=False)

    # Saving the converted audio in a mp3 file 
    myobj.save("./UPLOADS/convertedMessage.mp3")


    """ This portion Encrypts the Mp3 and saves to the outbound folder (using datetime) """
    # Generating key
    newKey = Fernet.generate_key()
    f = Fernet(newKey)
    # Writing newkey to outbound -- can remove later and just send to the user in text - TESTING ONLY
    with open('./UPLOADS/mykey.key', 'wb') as mykey:
        mykey.write(newKey)

    # Opening up original File
    with open('./UPLOADS/convertedMessage.mp3', 'rb') as original_file:
        original = original_file.read()

    # Encrypting
    encrypted = f.encrypt(original)

    # Saving to output
    with open ('./OUTBOUND/encryptedMessage.mp3', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    
    ## Below printing keys to console, only for testing -- disable for prd
    '''
    Example output:
    print(newKey) will be:  b'jxM5ubmiAzQ79PYH2XFjFCY0LbdturJvVlwzNQaJAlI='
    print(f) will be:       <cryptography.fernet.Fernet object at 0x7f248f769160>
    '''
    # print(newKey)
    # print(f)

    """ Key will be sent out via text here """
    

    """ All files in UPLOADS must be cleared out """




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

            """ This Will let the user download the file, then deletes all files in outbound """
            try:
                return send_from_directory("./OUTBOUND","encryptedMessage.mp3",as_attachment=True)
            except FileNotFoundError:
                os.abort(404)
            


    return render_template('upload.html', html_title = title, html_file = uploaded_file)

# # Download URL
# @app.route('/download/<path:path>',methods = ['GET','POST'])
# def download_file(path):
#     try:
#         return send_from_directory(OUTBOUND_FOLDER,path,as_attachment=True)
#     except FileNotFoundError:
#         os.abort(404)



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