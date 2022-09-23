def rsplitFunc (input):
    return input.rsplit(".",1)[1].lower()


output = rsplitFunc("Bingo.PNG.JPEG")
print(output)