
# first of all import the socket library
import socket					
 
# next create a socket object
s = socket.socket()			
print("Socket successfully created")

primary_ip = 
primary_port = 

backup_ip =
backup_port = 
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 10004				
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
s.bind(('192.168.0.10', port))		  
print("socket binded to "+ str(port))
s.setblocking(0)
# put the socket into listening mode
s.listen(5)	  
print("socket is listening")		

airport1 = []
airport2 = []
hotel 	 = [] # fill up ips here	  

# a forever loop until we interrupt it or 
# an error occurs
current_time = time.time()


while True:
 
	# Establish connection with client.
	c, addr = s.accept()	  
	print("Got connection from"+ str(addr) )
	msg = c.recv(1024)
	
	if(len(msg) !=0 ) :
		# send a thank you message to the client. 
		dicte = {}
		dicte['sender'] = 'heartbeat'
		dicte['address'] = [primary_ip,primary_port]

		c.send(json.dumps(dicte).encode('utf-8'))
		# Close the connection with the client
		c.close()


	if time.time() - current_time >5 :

		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setblocking(0)
		server.connect( (primary_ip,primary_port) )
		dicte = {}
		dicte['sender'] = 'heartbeat'
		server.send( json.dumps(dicte).encode('utf-8') )
		server.settimeout(5.0)
		msgg = server.recv()
		if len(msgg) == 0 :
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
			server_a1.setblocking(0)
			server_a2.setblocking(0)
			server_h.setblocking(0)


			dictee = {}
			dictee['sender'] = 'heartbeat'
			dictee['ip'] = primary_ip
			dictee['port'] = primary_port

			server_a1.connect(airport1[0],airport1[1])

			server_a2.connect(airport2[0],airport2[1])

			server_h.connect(hotel[0],hotel[1])

			current_time = time.time()


