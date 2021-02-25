#### Simple Encrypt Decrypt tools

This funny program services for encrypting and decrypting text manually.
For example it can be used for safe information transferring of plain text.


The program contains 2 py files for different tasks and json file (our dictionary for each "key")

1. EncryptDecrypt.py

This program is for encrypting some text or decrypting already encrypted text. The program uses particular json file
"LanguageDictionary.json". 

In this program we don't use "Space" like separate symbol, for more harder task
to decrypt our text :) Instead of this we use all double letters with space.

2 . DictCreator.py

This program is for creating new json-file instead of created. If you'll create new json file - nobody won't know 
which values you're using for your encrypt process. Even me :) 

**Be careful! Json file will be erased and changed just after opening DictCreator.py**