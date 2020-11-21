import socket
import sys
import time

clients = []

## end of imports ##
quit = False
## init ###

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
host = '192.168.1.100'
print("server will start on host: {0}".format(host))

port = 9090

print("Binding on {} : {} ... ".format(host, port))
s.bind((host, port))

print("Starting listening ...")
while not quit:
	try:
	    data, addr = s.recvfrom(1024)

	    if addr not in clients:
	    	clients.append(addr)
	    print(addr[0], addr[1], end="")
	    print(data.decode("utf-8"))

	    for client in clients:
	    	if addr != client:
	    		s.sendto(data, client)
	except:
		print("Server Stopped")
		quit = True
s.close()
