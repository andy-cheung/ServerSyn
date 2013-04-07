#center server, send the cmd to note srv
import socket
import sys
import os
import thread
import copy

def sendcmd(ip, cmd):
	port = 21000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port))
	s.send(cmd)
	print(s.recv(1024))
	#close socket finally
	s.close()

def waitforret(iplist):
	allip = copy.deepcopy(iplist)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket
	port = 21001
	s.bind(("0.0.0.0", port))
	s.listen(10)
	okcount, failcount = 0, 0
	while True:
		c, addr = s.accept()
		ip = addr[0]
		recvstr = c.recv(1024)
		c.close()

		strlist = recvstr.split(",")
		ret = "ok"
		cmd = ""
		if len(strlist) < 2:
			ret = "fail"
			failcount = failcount + 1
		else:
			cmd = strlist[0]
			ret = strlist[1]
			okcount = okcount + 1
		# recv a cmd, remove it from list 
		allip.remove(ip)

		# all return , this thread over
		if len(allip) <= 0:
			break

	print "all recv result, succ:%d, fail:%d" % (okcount, failcount)	
	s.close()

def startthread(cmd, allip) :
	thread.start_new_thread(waitforret, (allip, ))

if __name__ == '__main__':
	#arg1 is ip, arg2 is the cmd
	# if len(sys.argv) < 2:
	# 	print("arg less then 2")
	# 	os.exit(1)
	while True:
		cmd = sys.stdin.readline()[:-1]
		if cmd == "exit":
			sys.exit(0)
		elif cmd == "update":
			# update file every server
			# load ip list from file
			allip = []
			fp = open("iplist.txt", "r")		
			for line in fp.readlines():  
				line = line.strip('\n')
				allip.append(line)

			fp.close()

			allipcpy = copy.deepcopy(allip)
			startthread(cmd, allipcpy)
			for ip in allip:
				sendcmd(ip, cmd)	

