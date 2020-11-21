import os
import time

notfound = True
icon = ''
# python -m PyInstaller -F delcache1c.py "C:\Users\sa\Documents\py\бЄаЁЇв г¤ «Ґ­Ёп Єни  1б\delcache1c.py" 
os.system('title Reddidgy compiler for py-files v.1.0.3')
def compilefile(compstr):
	os.system(compstr)
	pass

currentloc = os.getcwd()
listfiles = os.listdir(path=".")

for filepy in listfiles:
	if filepy[-3:] == ".py" and notfound and filepy != 'compiler.py':
		notfound = False
		print('Trying to compile file', filepy)
		ask = input('(y/n):')
		if ask == 'n':
			notfound = True
		elif ask == 'y':
			for file2 in listfiles:
				if file2[-4:] == ".ico":
					ask2 = input('Do you want use {} like icon file? (y/n):'.format(file2))
					if ask2 == 'y':
						icon = ' -i ' + '"' + file2 + '"'
					if ask2 == 'n':
						continue
			compstr = 'python -m PyInstaller -F ' + '"' + filepy + '"' + ' ' + '"' + currentloc + '\\' + filepy + '"' + icon
			compilefile(compstr)
			#print(compstr)
		else:
			continue

		
		
