#center server, send the cmd to note srv
import socket
import sys
import os

if __name__ == '__main__':
	port = 21000
	if len(sys.argv) < 1:
		print("arg less then 1")
		os.exit(1)

	s = socket.socket()
	s.connect((sys.argv[1], port))
	s.send("update")
	print(s.recv(1024))
	#close socket finally
	s.close()


