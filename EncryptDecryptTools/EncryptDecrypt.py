## INFO
## ==========================================
## The program encrypts text using dictionary file "LanguageDictionary.json"
## EncrypterDecrypter doesn't use Space like separate symbol to complicate manual decrypt master :)
## Instead of this we're using common characters with space like separate dictionary items
##
## "a" : "value"
## "a " : "differentValue"


try:
    import json
except:
    print("Use pip install json")               # Trying to import json
    quit()

try:
    filename = "LanguageDictionary.json"        # Trying to get dictionary file and write to variable
    filename_opened = open(filename,mode='r')
    j = {}
    j = json.load(filename_opened)
    filename_opened.close()
except:
    print("Dictionary file for encrypt/decrypt doesn't exist!")
    print("Filename: " + filename)
    print("Put your dictionary file to folder with py files or create it using DictCreator.py")
    quit()

chars = ""              # Creates String with all chars for encrypt or decrypt
for i in j.keys():          # (it's just for comfortable use in some methods)
    chars += i

def Menu():                             # simple menu func in console
    print("1. Decrypt the text")
    print("2. Encrypt the text")
    print("----------------------------")
    opt = input(": ")
    if opt == "1":
        DecryptText()
    elif opt == "2":
        EncryptText()
    else:
        print("Wrong command")
        return

def EncryptText():            # EncryptFunc
    print("Note: The encrypter can can use RU/EN language and some special symbols.")
    print("If symbols doesn't using here the crypter will miss it.")
    normalText = input("Enter text to crypt: ").lower()     # we don't use high symbols for comfortable.
    cryptedText = ""
    for i in range(0, len(normalText)):
        if normalText[i] != " " and normalText[i] in chars:  # if current char is not space
            if normalText[i] in chars:                       # if we have char in chars string
                if i != len(normalText) - 1:                 # rechecking for last symbol
                    if normalText[i + 1] == " ":  # If we have " " after symbol we'll assign other dict key
                        char = normalText[i] + " "
                        if char not in j.keys():            # If we have symbol with space but we don't have that symbol in our dict
                            char = normalText[i]                # than we're just using normal symbol w/o space
                    else:
                        char = normalText[i]
                else:
                    char = normalText[i]
                cryptedText = cryptedText + j[char]
    print("Text to crypt: ")
    print(normalText)
    print("Crypted text: ")
    print(cryptedText)
    return

def DecryptText():
    cryptedText = input("Enter crypted text: ")
    decryptedText = ""
    indexCount = -1
    if (len(cryptedText) % 4) == 0:
        for i in cryptedText:
            indexCount = indexCount + 1
            if (indexCount % 4) == 0:
                cryptedValue = cryptedText[indexCount] + cryptedText[indexCount + 1] + cryptedText[indexCount + 2] + \
                               cryptedText[indexCount + 3]
                if cryptedValue not in j.values():
                    print("Invalid value for symbol")
                else:
                    for key, value in j.items():
                        if value == cryptedValue:
                            decryptedText += key
    else:
        print("Invalid crypted value!")
    print(decryptedText)
    return

############### Main cycle ###########################

while True:
    Menu()