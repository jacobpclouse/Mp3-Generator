 # converts the text to speech  
import pyttsx3

# Imports PIL module 
from PIL import Image

# will convert the image to text string
import pytesseract 

  
# open method used to open different extension image file
im = Image.open(r"./Sample Text Examples/sample text 2.png") 
im2 = Image.open(r"./Sample Text Examples/text15.png") 
im3 = Image.open(r"./Sample Text Examples/Favicon.png") 
im4 = Image.open(r"./Sample Text Examples/logo.png") 
  
# This method will show image in any image viewer 
#im.show() 
#im2.show()

print(im)
print(im2)


result = pytesseract.image_to_string(im4) 
#print(result)
# write text in a text file and save it to source path   
with open('./Output/outputText.txt',mode ='w') as file:     
      
                 file.write(result)
                 print(result)

if result == "":
	print("its empty")
else: 
	print(result)

print("Got to end")

"""
# import the following libraries
# will convert the image to text string
import pytesseract	

# adds image processing capabilities
from PIL import Image	

# converts the text to speech
import pyttsx3		

#translates into the mentioned language
from googletrans import Translator	

# opening an image from the source path
img = Image.open('text1.png')	

# describes image format in the output
print(img)						
# path where the tesseract module is installed
pytesseract.pytesseract.tesseract_cmd ='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
# converts the image to result and saves it into result variable
result = pytesseract.image_to_string(img)
# write text in a text file and save it to source path
with open('abc.txt',mode ='w') as file:	
	
				file.write(result)
				print(result)
				
p = Translator()					
# translates the text into german language
k = p.translate(result,dest='german')	
print(k)
engine = pyttsx3.init()

# an audio will be played which speaks the test if pyttsx3 recognizes it
engine.say(k)							
engine.runAndWait()

"""