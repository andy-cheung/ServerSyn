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

def process(cmd, ip):
	print "cmd:" + cmd
	if cmd == "update":
		# update file from file center
		print("update")
		os.system("./update.sh")
	elif cmd == "start":
		# start all game server
		print("start")
	# call back the center server 
	ret = "ok"
	sendresult(cmd, ip, ret)

def sendresult(cmd, ip, ret):
	port = 21001
	s = socket.socket()
	s.connect((ip, port))
	s.send(cmd + "," + ret)
	s.close()	

if __name__ == '__main__':
	startSrv()
	print("startSrv success!")

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket
	port = 21000
	s.bind(("0.0.0.0", port))
	s.listen(10)
	while True:
		c, addr = s.accept()
		ip = addr[0]
		cmd = c.recv(1024)
		c.send("recv ok")
		c.close()

		print "recv cmd:%s, from:%s" % (cmd, ip)
		#process the cmd
		process(cmd, ip)
