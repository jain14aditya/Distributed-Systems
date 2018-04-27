# first of all import the socket library
import socket	 
import json			  
import select
import MySQLdb
# next create a socket object
airport1 = socket.socket()			
print "Socket successfully created"
 
# reserve a port on your computer in our
# case it is 1245 but it can be anything
port = 10000			  
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
airport1.bind(('192.168.0.10',port))		  
print "socket binded to %s" %(port)
 
# put the socket into listening mode
airport1.listen(5)	  
print "socket is listening"			 
 
# a forever loop until we interrupt it or 
# an error occurs

inputs = [airport1]
outputs = []
message_queues = {}


while True:
 
	readable, writable, exceptional = select.select(inputs, outputs, inputs)
	# Establish connection with client.
	for s in readable:

		if s is airport1:
			c, addr = airport1.accept() 
			print 'Got connection from',c,addr
			
		else:
			msg = c.recv(1024)
			print msg
			dict= json.loads(msg.decode('utf-8'))
			for i in dict:
				print i,"\t = ",dict[i]
			# print(dict)

			if dict['type'] == 0 :
				db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                    user="root",         # your username
                    passwd="root",  # your password
                    db="distributed_systems")

				cur = db.cursor()
				# print (dict['people'],dict['from'],dict['to'],dict['Date'])
				cur.execute('update airport1_temp set tickets = %s where from_loc = %s and to_loc = %s and date_ = %s', (10,dict['from'],dict['to'],dict['Date']))
				# db.commit()

				# cur.execute('select tickets,cost from airport1_temp where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				cur.execute('select * from airport1_temp where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				for row in cur.fetchall():
					print row

			# s.close()		





	# if(len(msg) ==0 ) :
	# 	continue

	# c is the connection , conn.recv will read as many bytes as possible
	# database will be queried and message will be sent 

	# send a thank you message to the client. 
	# c.send('Thank you for connecting')
 
	# Close the connection with the client
	# c.close()

	# print(" You want to continue or not ") 
	

