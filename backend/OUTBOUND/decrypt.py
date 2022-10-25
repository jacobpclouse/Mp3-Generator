# source: https://towardsdatascience.com/encrypt-and-decrypt-files-using-python-python-programming-pyshark-a67774bbf9f4
# check to see if a file exists: https://www.pythontutorial.net/python-basics/python-check-if-file-exists/#:~:text=To%20check%20if%20a%20file%20exists%2C%20you%20pass%20the%20file,path%20standard%20library.&text=If%20the%20file%20exists%2C%20the,Otherwise%2C%20it%20returns%20False%20


###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
### IMPORTS: 
###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
from cryptography.fernet import Fernet # will be used for encrypting output
import os.path


###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
### FUNCTIONS
###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# --- Function to print out my Logo ---
def myLogo():
    print("Created and Tested by: ")
    print("   __                  _         ___ _                       ")
    print("   \ \  __ _  ___ ___ | |__     / __\ | ___  _   _ ___  ___  ")
    print("    \ \/ _` |/ __/ _ \| '_ \   / /  | |/ _ \| | | / __|/ _ \ ")
    print(" /\_/ / (_| | (_| (_) | |_) | / /___| | (_) | |_| \__ \  __/ ")
    print(" \___/ \__,_|\___\___/|_.__/  \____/|_|\___/ \__,_|___/\___| ")




'''
-=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=-=
-=-=-=-=-=-=--=-=-=-=-=-=- MAIN PROGRAM -=-=-=-=-=-=--=-=-=-=-=-=-
-=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=-=
'''
#Check to see if the key file is in the local directory
doesExist = os.path.exists('./mykey.key')
print(doesExist)



###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
###IF the key exists, use it to decrypt
###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
if doesExist == True:
    print("KEY EXISTS!")
    ## OPENING UP THE KEY
    with open('./mykey.key', 'rb') as key_file:
        theKey = key_file.read()

        f = Fernet(theKey)


###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
### If key doesn't exist, then ask user
###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
else:
    print("KEY DOES NOT EXIST")
    userInput = input("Enter in your key: ")

    f = Fernet(userInput)


## OPENING UP ENCRYPTED MESSAGE
with open('./encryptedMessage.mp3', 'rb') as encrypted_file:
    encrypted = encrypted_file.read()

## DECRYPTING
decrypted = f.decrypt(encrypted)

## SAVING DECRYPTED MESSAGE
with open('decryptedMessage.mp3', 'wb') as decrypted_file:
    decrypted_file.write(decrypted)



###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
### END
###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
myLogo()
print("All done!")