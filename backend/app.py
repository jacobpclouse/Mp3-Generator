# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
from enum import unique
import os,shutil
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image # Imports PIL module 
import pytesseract # will convert the image to text string
from gtts import gTTS # Import module for text to speech conversion
from cryptography.fernet import Fernet # will be used for encrypting output
import base64
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
import datetime
from zipfile import ZipFile
from os.path import basename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


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


# Database setup 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init the Database
db = SQLAlchemy(app)

# Create Database model -- Will make fields required later
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True,nullable=False)
    mp3Username = db.Column(db.String(200),nullable=False)
    mp3UserPassword = db.Column(db.String(200),nullable=False)
    mp3UserPhone = db.Column(db.Float(10),nullable=False)
    mp3UserEmail = db.Column(db.String(120),nullable=False)

    # function to return string when added to db
    def __repr__(self):
        return "<mp3Username %r" % self.id

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":","_")
    current_datetime = current_datetime.replace(".","-")
    current_datetime = current_datetime.replace(" ","_")
    
    return current_datetime

# used to find ending type for file AND checking to make sure that it is an allowed type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# used to find ending type for file only (for creating temp pic in UPLOADS)
def getExtension(inputFile):
    return '.' and inputFile.rsplit(".",1)[1].lower()


# copy readme and decrypt to the OUTBOUND folder and zip all the files (use "OUTBOUND")
def copyAndZip(destinationDirectory,outputZipFileName,originDirectory):
    files = [f'{originDirectory}decrypt.py', f'{originDirectory}readme.txt']
    for f in files:
        shutil.copy(f, destinationDirectory)

    #shutil.make_archive(outputZipFileName, 'zip', destinationDirectory)
    with ZipFile(f'{outputZipFileName}.zip','w') as myzip:
        print("get all files in this directory")
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(destinationDirectory):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                myzip.write(filePath, basename(filePath))


# Function to send email with attachment
def sendEmailFunc(sendFROMemail,sendTOemail,subjectLine,contentOfMessage,attachmentName,DesiredFilename,firstName,lastName):

    current_datetime = defang_datetime() #getting datetime for the name of the file

    # opening the file/decoding/saving it
    with open(f'{attachmentName}', 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()    

    # saving api key in the environment
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

    from_email = Email(f"{sendFROMemail}")  # Change to your verified sender
    to_email = To(f"{sendTOemail}")  # Change to your recipient
    subject = f"{subjectLine}-{firstName} {lastName}"
    #content = Content("text/plain", f"{contentOfMessage}")
    html_content=Content('text/html', f'<h1>{firstName}, Thank you for using JPC Converter / Encryptor!</h1><p>{contentOfMessage}</p><p><b>Date Sent: {current_datetime}</b></p>')
    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(f'{current_datetime}__{DesiredFilename}'),
        FileType('mp3'), # try removing this, does it still work?
        Disposition('attachment')
    )

    mail = Mail(from_email, to_email, subject, html_content)
    mail.attachment = attachedFile  # tacking on the attachment

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)


# will open the pic file in the uploads folder, convert to text, then convert text to mp3
def openPic(filenameAndExtenstion,userEmail,firstName,lastName):

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
    
    # Copy decrypt and readme to the outboud directory and then zip them
    outgoingZip = 'Encrypted MP3 Conversion Archive & Data'
    copyAndZip('./OUTBOUND',outgoingZip,'./IMPORTANT_FILES/')

    ## Below printing keys to console, only for testing -- disable for prd
    '''
    Example output:
    print(newKey) will be:  b'jxM5ubmiAzQ79PYH2XFjFCY0LbdturJvVlwzNQaJAlI='
    print(f) will be:       <cryptography.fernet.Fernet object at 0x7f248f769160>
    '''
    # print(newKey)
    # print(f)

    """ Data for email will be set here """
    print("Starting Sending Email...")
    sourceEmail = "mp3converterandencryptor@gmail.com"
    outboundEmail = userEmail

    subjectOfEmail = "Here is Your Converted MP3!"
    contentOfEmail = "Your file will be attached below, you need to decrypt it with your key before you can listen to it."
    #attachmentOfEmail = "./OUTBOUND/encryptedMessage.mp3" 
    #desiredEmailFilename = "encryptedMessage.mp3"
    attachmentOfEmail = f"{outgoingZip}.zip" 
    desiredEmailFilename = f"{outgoingZip}.zip"

    sendEmailFunc(sourceEmail,outboundEmail,subjectOfEmail,contentOfEmail,attachmentOfEmail,desiredEmailFilename,firstName,lastName)
    print("Finished Sending Email!")

    """ Key will be sent out via text here """
    

    """ All files in UPLOADS must be cleared out """




## NEED DELETE function or to add it all on to an existing function

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# @app.route('/')
# def mainRouteFunc():
#     return render_template('base.html')

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
            # GRABBING FORM INFO -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            # getting input with name = fname in HTML form
            first_name = request.form.get("fname")
            # getting input with name = lname in HTML form
            last_name = request.form.get("lname")
            # getting input with email = userEmail in HTML form
            form_email = request.form.get("userEmail")
            # getting input with email = userEmail in HTML form
            form_phone = request.form.get("userPhone")

            print(f"User's Name: {first_name} {last_name}")
            print(f"User's Phone: {form_phone}")

            secureTheFile = secure_filename(file.filename)
            extensionType = getExtension(secureTheFile)

            # Filename below - Important for functions 
            filename = "Temp_Pic_Upload." + extensionType
                    #filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_file = secureTheFile
                    ##return redirect(url_for('download_file', name=filename))

            # function to convert to text, convert to mp3, encrypt and clean up UPLOADS
            openPic(filename,form_email,first_name,last_name)

            """ This Will let the user download the file, then deletes all files in outbound """
            try:
                #return send_from_directory("./OUTBOUND","encryptedMessage.mp3",as_attachment=True)
                return send_from_directory("./UPLOADS","mykey.key",as_attachment=True)
            except FileNotFoundError:
                os.abort(404)

            

    return render_template('upload.html', html_title = title, html_file = uploaded_file)


# # Login Url -- redirect here if not authenticated
@app.route('/',methods = ['GET','POST'])
@app.route('/login',methods = ['GET','POST'])
def login():
    title = "You need to Login"

    if request.method == "POST":
        user_username = request.form["html_username"]
        user_password = request.form["html_password"]

        # print(f"Username is: {user_username}")
        # print(f"Username is: {user_password}")

    # NEED TO HAVE A CHECK TO LOOK AT DATABASE AND SEE IF THE USER EXISTS

    # else: 
    return render_template('login.html', html_title = title)



@app.route('/signup')
def signup():
    title = "You need to Sign Up"
    return render_template('signup.html', html_title = title)


# Use flask templates for logic, linking and overall tutorials
# https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application#step-4-using-conditionals-and-loops
# THEN build out backend, add frontend/then bootstrap and angular