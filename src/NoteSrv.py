#accept cmd from the center server and process it
import socket
import os
import sys

def startSrv():
	try:
		pid = os.fork()
		if pid > 0:
			sys.exit(0)
	except Exception, e:
		sys.stderr.write("fork 1 fail -->%d --> %s\n" % (e.errno, e.strerror))
		sys.exit(1)
	os.chdir("/")
	os.setsid()
	os.umask(0)

	try:
		pid = os.fork()
		if pid > 0:
			sys.exit(0)
	except Exception, e:
		sys.stderr.write("fork 2 fail -->%d --> %s\n" % (e.errno, e.strerror))
		sys.exit(1)

	sys.stdout.flush()
	sys.stderr.flush()

if __name__ == '__main__':
	startSrv()
	print("startSrv success!")
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket
	host = socket.gethostname()
	port = 21000
	s.bind((host, port))
	s.listen(10)
	while True:
		c, addr = s.accept()
		c.send("hahahahah")
		c.close()
