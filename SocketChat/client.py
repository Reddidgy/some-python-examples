import socket
import threading
import time

shutdown = False
join = False

def receving(name, sock):
	while not shutdown:
		try:
			while True:
				data, addr = sock.recvfrom(1024)
				print(data.decode("utf-8"))
				time.sleep(0.2)
		except:
			pass

#host = socket.gethostbyname(socket.gethostname())
#host = socket.gethostbyname(socket.getfqdn())

host = ''
port = 0

server = ('83.167.10.9', 9090)

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

alias = str(input("Name: "))

rT = threading.Thread(target= receving, args =("RecvThread",s))
rT.start()

while shutdown == False:
	if join == False:
		#print(server)
		s.sendto(("["+alias + "] => join chat ").encode("utf-8"),server)
		join = True
	else:
		try:
			message = str(input())

			if message != "":
				s.sendto(("["+alias + "] :: "+message).encode("utf-8"),server)
			time.sleep(0.2)
		except:
			s.sendto(("["+alias + "] <= left chat ").encode("utf-8"),server)
			shutdown = True
rT.join()
s.close()