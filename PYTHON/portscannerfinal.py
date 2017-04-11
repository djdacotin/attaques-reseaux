import socket

hosts = ["10.0.0.1", "10.0.0.2"]

lowPort = 1
highPort = 65535
#ports = [22, 23, 80, 443, 445, 3389]
ports = range(lowPort, highPort)

for host in hosts:
	print "[+] Connecting to " + host 
	for port in ports:
		try:
		    #print "[+] Connecting to " + host + ":" + str(port)
	            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	            s.settimeout(5)
	            result = s.connect_ex((host, port))
	            if result == 0:
	                print "  [*] Port " + str(port) + " open!"
	            s.close()
	        except:
	            pass
