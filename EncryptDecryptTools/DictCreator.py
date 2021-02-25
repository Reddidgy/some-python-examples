import json
from random import randint

chars = "qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбюё!?.,:()@#$%^&*1234567890й ц у к е н г ш щ з х ъ ф ы в а п р о л д ж э я ч с м и т ь б ю ё q w e r t y u i o p a s d f g h j k l z x c v b n m 1 2 3 4 5 6 7 8 9 0"
charsWithSpaces = ""
cryptedSymbolValue = ""

cryptChars = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*(){}:<>"

readyDict = {}              # Dictionary for json.dump with all new values(encrypted) to each key(symbol)
indexCount = -1

#
for c in chars:
    if indexCount <= 81:  # last index symbol without space
        indexCount = indexCount + 1
        cryptedSymbolValue = ""
        for i in range(0, 4):
            cryptedSymbolValue += cryptChars[randint(0, len(cryptChars) - 1)]

        if cryptedSymbolValue not in readyDict.values():        # re-check for double 1 time. It's enough :)
            readyDict.update({c: cryptedSymbolValue})
            print("symbol: " + c + " index: " + str(indexCount) + " cryptedValue: " + cryptedSymbolValue)
        else:
            print("Unexpected repeat!")
            for i in range(0, 4):
                cryptedSymbolValue += cryptChars[randint(0, len(cryptChars) - 1)]
            readyDict.update({c: cryptedSymbolValue})
            print("symbol: " + c + " index: " + str(indexCount) + " cryptedValue: " + cryptedSymbolValue)

    else:                               # Filling symbols with space (for harder task for potential decrypters)
        indexCount = indexCount + 1
        if c != " ":
            print("current index is " + str(indexCount))
            cryptedSymbolValue = ""
            for i in range(0, 4):
                cryptedSymbolValue += cryptChars[randint(0, len(cryptChars) - 1)]
            print("symbol: " + c + "  index: " + str(indexCount) + " cryptedValue: " + cryptedSymbolValue)
            readyDict.update({c + " ": cryptedSymbolValue})


print(readyDict)
fileToRecord = "LanguageDictionary.json"
filename_opened = open(fileToRecord, mode='w')

json.dump(readyDict, filename_opened)
filename_opened.close()
