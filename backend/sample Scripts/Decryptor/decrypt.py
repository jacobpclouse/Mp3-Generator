# source: https://towardsdatascience.com/encrypt-and-decrypt-files-using-python-python-programming-pyshark-a67774bbf9f4

from cryptography.fernet import Fernet # will be used for encrypting output

## OPENING UP THE KEY
with open('./mykey.key', 'rb') as key_file:
    theKey = key_file.read()

f = Fernet(theKey)

## OPENING UP ENCRYPTED MESSAGE
with open('./encryptedMessage.mp3', 'rb') as encrypted_file:
    encrypted = encrypted_file.read()

## DECRYPTING
decrypted = f.decrypt(encrypted)

## SAVING DECRYPTED MESSAGE
with open('decryptedMessage.mp3', 'wb') as decrypted_file:
    decrypted_file.write(decrypted)