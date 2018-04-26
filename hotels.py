# first of all import the socket library
import socket	 
import json			  
import select

# next create a socket object
s = socket.socket()			
print "Socket successfully created"
 
# reserve a port on your computer in our
# case it is 1245 but it can be anything
port = 10002		
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
s.bind(('192.168.0.10',port))		  
print "socket binded to %s" %(port)
 
# put the socket into listening mode
s.listen(5)	  
print "socket is listening"			 
 
# a forever loop until we interrupt it or 
# an error occurs
while True:
 
	# Establish connection with client.
	c, addr = s.accept() 

	print 'Got connection from', addr

	msg = c.recv(1024)
	if(len(msg) ==0 ) :
		continue

	dict= json.loads(msg.decode('utf-8'))
	print(type(dict))
	print(dict)
	# c is the connection , conn.recv will read as many bytes as possible

	# send a thank you message to the client. 
	c.send('Thank you for connecting')
 
	# Close the connection with the client
	c.close()

	print(" You want to continue or not ") 
	#a = 

