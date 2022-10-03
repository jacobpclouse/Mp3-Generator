## https://docs.sendgrid.com/for-developers/sending-email/quickstart-python#complete-code-block
# https://stackoverflow.com/questions/39717986/httperror-http-error-401-unauthorized-for-sendgrid-integration-with-python

# importing library
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

# make sure to set environment variable before you do this

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Functions
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


# Function to send email
def sendEmailFunc(sendFROMemail,sendTOemail,subjectLine,contentOfMessage):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    #sg = sendgrid.SendGridAPIClient(api_key)
    from_email = Email(f"{sendFROMemail}")  # Change to your verified sender
    to_email = To(f"{sendTOemail}")  # Change to your recipient
    subject = f"{subjectLine}"
    content = Content("text/plain", f"{contentOfMessage}")
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Main
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


# This is where the information is gathered from the user to craft email
# mp3converterandencryptor@gmail.com 
sourceEmail = input("What email are your sending this from: ")
outboundEmail = input("Who are we sending this to: ")

subjectOfEmail = input("What is the Subject line: ")
contentOfEmail = input("What content do you want in this email: ")


sendEmailFunc(sourceEmail,outboundEmail,subjectOfEmail,contentOfEmail)

print("DONEZO!")