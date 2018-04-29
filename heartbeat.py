
# first of all import the socket library
import socket					
import time
import json
import threading

# next create a socket object

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setblocking(0)
		
print("Socket successfully created")

primary_ip = '0.0.0.0'
primary_port = 12559

backup_ip = '0.0.0.0'
backup_port = 12560
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 10004				
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
s.bind(('0.0.0.0', port))		  
print("socket binded to "+ str(port))
#s.setblocking(0)
# put the socket into listening mode
s.listen(5)	  
print("socket is listening")		

airport1 = ['0.0.0.0',10000]
airport2 = ['0.0.0.0',10001]
hotel 	 = ['0.0.0.0',10002] # fill up ips here	  

# a forever loop until we interrupt it or 
# an error occurs
current_time = time.time()


#while True:
def waitmsg():
	while  True:
		# Establish connection with client.
		c, addr = s.accept()
		#s.setblocking(0)	  
		print("Got connection from"+ str(addr) )
		# send a thank you message to the client. 
		dicte = {}
		dicte['sender'] = 'heartbeat'
		dicte['address'] = [primary_ip,primary_port]

		c.send(json.dumps(dicte).encode('utf-8'))
		# Close the connection with the client
		#c.close()





#while True
def writemsg():
	global current_time
	global primary_ip
	global primary_port
	global backup_ip
	global backup_port
	if time.time() - current_time > 5 :

		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#server.setblocking(0)
		try:
			server.connect( (primary_ip, primary_port) )
			dicte = {}
			dicte['sender'] = 'heartbeat'
			server.send( json.dumps(dicte).encode('utf-8') )
			server.settimeout(5.0)
			msgg = server.recv(1024)
		except:
			# server has failed change ips and ports

			temp_ip = primary_ip
			primary_ip = backup_ip
			backup_ip = temp_ip


			temp_port = primary_port
			primary_port = backup_port
			backup_port = temp_port

			server_a1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_a2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_h = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			#server_a1.setblocking(0)
			#server_a2.setblocking(0)
			#server_h.setblocking(0)


			dictee = {}
			dictee['sender'] = 'heartbeat'
			dictee['ip'] = primary_ip
			dictee['port'] = primary_port

			server_a1.connect((airport1[0],airport1[1]))

			server_a2.connect((airport2[0],airport2[1]))

			server_h.connect((hotel[0],hotel[1]))

			server_a1.send(json.dumps(dictee).encode('utf-8'))
			server_a2.send(json.dumps(dictee).encode('utf-8'))
			server_h.send(json.dumps(dictee).encode('utf-8'))
		current_time = time.time()
		server.close()

try:
	t1 = threading.Thread(name='waitmsg', target=waitmsg)
	t1.start()
except:
	print "Thread 1 error"

while  True:
		
	try:
		# threads = []

		# Create new threads
		t2 = threading.Thread(name='writemsg', target=writemsg)
		# Start new Threads
		t2.start()

		# # Add threads to thread list
		# threads.append(t1)
		# threads.append(t2)

		# Wait for all threads to complete
		t2.join()
	except:
	   print "Error: unable to start thread"