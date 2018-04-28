# first of all import the socket library
import socket	 
import json			  
import select
import MySQLdb
import Queue
# next create a socket object
airport2 = socket.socket()			
print "Socket successfully created"
 
# reserve a port on your computer in our
# case it is 1245 but it can be anything
port = 10001			  
 

# Create a TCP/IP socket
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '10.102.61.204'
server_host = 12559

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
airport2.bind(('10.102.61.204',port))		  
print "socket binded to %s" %(port)
 
# put the socket into listening mode
airport2.listen(5)	  
print "socket is listening"			 
 
# a forever loop until we interrupt it or 
# an error occurs

inputs = [airport2]
outputs = []
message_queue = {}


while True:
 
	readable, writable, exceptional = select.select(inputs, outputs, inputs)
	# Establish connection with client.
	for s in readable:

		if s is airport2:
			print "\n\n =========== SERVER listening ================="
			c, addr = airport2.accept() 
			print 'Got connection from',addr
			c.setblocking(0)
			inputs.append(c)
			# Give the connection a queue for data we want to send
			message_queue[c] = Queue.Queue()
			print "=========== SERVER part over ================="


		else:
			print "\n\n +++++++ Query Processing ++++++++"
			msg = s.recv(1024)
			# print msg
			# print type(msg)
			dict= json.loads(msg.decode('utf-8'))
			# for i in dict:
			# 	print i,"\t = ",dict[i]
			print(dict)

			if dict['sender'] == 'heartbeat' :
				# now we need to update it from the message it sent
				server_ip = dict['ip']
				server_host = dict['port']
				inputs.remove(s)
				continue


			if dict['type'] == 1 :
				print "\n\n----------------- Type1 started ---------------"
				print "read type from permanent"
				db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                    user="root",         # your username
                    passwd="root",  # your password
                    db="distributed_systems")

				cur = db.cursor()
				# print (dict['people'],dict['from'],dict['to'],dict['Date'])
				# cur.execute('update airport2_temp set tickets = %s where from_loc = %s and to_loc = %s and date_ = %s', (dict['people'],dict['from'],dict['to'],dict['Date']))
				# db.commit()
				print dict['from'],dict['to'],dict['Date']
				# cur.execute('select tickets,cost from airport2_temp where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				cur.execute('select tickets,cost from airport2_perm where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				
				dicte = {}
					
  				for row in cur.fetchall():
					print row
					dicte['sender'] = 'airport_2'
					dicte['flag'] = 1
					dicte['ticket'] = row[0]
					dicte['cost'] = row[1]
					dicte['index'] = dict['index']
					dicte['pos'] = 2
					dicte['type']= dict['type']
					dicte['id'] = dict['id']
					# dicte['client_ip'] = dict['client_ip']
					# dicte['client_port'] = dict['client_port']
					break

				inputs.remove(s)
				outputs.append(s)
				print dict
				message_queue[s].put(dicte)		
				print "----------------- Type1 finished---------------"
				# "------- Query Processing -------"

			elif dict['type'] == 2 :
				print "\n\n----------------- Type2 started ---------------"
				print "writing to temp"
				db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                    user="root",         # your username
                    passwd="root",  # your password
                    db="distributed_systems")

				cur = db.cursor()
				# print (dict['people'],dict['from'],dict['to'],dict['Date'])
				# cur.execute('update airport2_temp set tickets = %s where from_loc = %s and to_loc = %s and date_ = %s', (dict['people'],dict['from'],dict['to'],dict['Date']))
				# db.commit()

				# cur.execute('select tickets,cost from airport2_temp where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				cur.execute('select tickets,cost from airport2_temp where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				
				dicte = {}
					
  				for row in cur.fetchall():
					print row
					dicte['sender'] = 'airport_2'
					dicte['flag'] = 1
					dicte['ticket'] = row[0]
					dicte['cost'] = row[1]
					dicte['index'] = dict['index']
					dicte['pos'] = 2
					dicte['type']= dict['type']
					dicte['id'] = dict['id']
					# dicte['client_ip'] = dict['client_ip']
					# dicte['client_port'] = dict['client_port']
					break
				print "ticket = ",dicte['ticket'], " people = ",dict['people']
				if int(dicte['ticket']) < int(dict['people']) : 
					# then it is not possible to book ticket here
					dicte['flag'] = -2 
				else :
					# print "else part"
					val = int(dicte['ticket']) - int(dict['people'])
					print "val = ",val 
					cur.execute('update airport2_temp set tickets = %s where from_loc = %s and to_loc = %s and date_ = %s', (val,dict['from'],dict['to'],dict['Date']))
					db.commit()
					cur.execute('select tickets,cost from airport2_temp where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
					for row1 in cur.fetchall():
						print row1
				
				inputs.remove(s)
				outputs.append(s)
				message_queue[s].put(dicte)	
				print "----------------- Type2 ended ---------------"

			elif dict['type'] == 3 :
				print "\n\n----------------- Type3 started ---------------"
				print "remove tickets in airport2_temp"
				db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                    user="root",         # your username
                    passwd="root",  # your password
                    db="distributed_systems")

				cur = db.cursor()
				# print (dict['people'],dict['from'],dict['to'],dict['Date'])
				# cur.execute('update airport2_temp set tickets = %s where from_loc = %s and to_loc = %s and date_ = %s', (dict['people'],dict['from'],dict['to'],dict['Date']))
				# db.commit()

				# cur.execute('select tickets,cost from airport2_temp where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				cur.execute('select tickets,cost from airport2_perm where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				
				dicte = {}
					
  				for row in cur.fetchall():
					print row
					dicte['sender'] = 'airport_2'
					dicte['flag'] = 1
					dicte['ticket'] = row[0]
					dicte['cost'] = row[1]
					dicte['index'] = dict['index']
					dicte['pos'] = 2
					dicte['type']= dict['type']
					dicte['id'] = dict['id']
					# dicte['client_ip'] = dict['client_ip']
					# dicte['client_port'] = dict['client_port']
					break

				# print "ticket = ",dicte['ticket'], " people = ",dict['people']
				if int(dicte['ticket']) < int(dict['people']) : 
					# then it is not possible to book ticket here
					dicte['flag'] = -2 
				else :
					# print "else part"
					val = int(dicte['ticket']) - int(dict['people'])
					print "val = ",val 
					cur.execute('update airport2_perm set tickets = %s where from_loc = %s and to_loc = %s and date_ = %s', (val,dict['from'],dict['to'],dict['Date']))
					db.commit()
					cur.execute('select tickets,cost from airport2_perm where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
					for row1 in cur.fetchall():
						print row1
				inputs.remove(s)
				outputs.append(s)

				message_queue[s].put(dicte)	
				print "----------------- Type3 ended ---------------"

			elif dict['type'] == 4 :
				print "\n\n----------------- Type4 started ---------------"
				print "reverting back the changes from temp database"
				db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                    user="root",         # your username
                    passwd="root",  # your password
                    db="distributed_systems")

				cur = db.cursor()
				# print (dict['people'],dict['from'],dict['to'],dict['Date'])
				# cur.execute('update airport2_temp set tickets = %s where from_loc = %s and to_loc = %s and date_ = %s', (dict['people'],dict['from'],dict['to'],dict['Date']))
				# db.commit()

				# cur.execute('select tickets,cost from airport2_temp where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				cur.execute('select tickets,cost from airport2_temp where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				
				dicte = {}
					
  				for row in cur.fetchall():
					print row
					dicte['sender'] = 'airport_2'
					dicte['flag'] = 1
					dicte['ticket'] = row[0]
					dicte['cost'] = row[1]
					dicte['index'] = dict['index']
					dicte['pos'] = 2
					dicte['type']= dict['type']
					dicte['id'] = dict['id']
					# dicte['client_ip'] = dict['client_ip']
					# dicte['client_port'] = dict['client_port']
					break


				val = int(dicte['ticket']) + int(dict['people'])
				print "val = ",val 
				cur.execute('update airport2_temp set tickets = %s where from_loc = %s and to_loc = %s and date_ = %s', (val,dict['from'],dict['to'],dict['Date']))
				db.commit()
				cur.execute('select tickets,cost from airport2_temp where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				for row1 in cur.fetchall():
					print row1
				inputs.remove(s)
				outputs.append(s)

				message_queue[s].put(dicte)	
				print "----------------- Type4 ended ---------------"

			elif dict['type'] == 5 :
				print "\n\n----------------- Type5 started ---------------"
				print "reverting back the changes from temp database"
				db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                    user="root",         # your username
                    passwd="root",  # your password
                    db="distributed_systems")

				cur = db.cursor()
				# print (dict['people'],dict['from'],dict['to'],dict['Date'])
				# cur.execute('update airport2_temp set tickets = %s where from_loc = %s and to_loc = %s and date_ = %s', (dict['people'],dict['from'],dict['to'],dict['Date']))
				# db.commit()

				# cur.execute('select tickets,cost from airport2_temp where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				cur.execute('select tickets,cost from airport2_perm where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				
				dicte = {}
					
  				for row in cur.fetchall():
					print row
					dicte['sender'] = 'airport_2'
					dicte['flag'] = 1
					dicte['ticket'] = row[0]
					dicte['cost'] = row[1]
					dicte['index'] = dict['index']
					dicte['pos'] = 2
					dicte['type']= dict['type']
					dicte['id'] = dict['id']
					# dicte['client_ip'] = dict['client_ip']
					# dicte['client_port'] = dict['client_port']
					break


				val = int(dicte['ticket']) + int(dict['people'])
				print "val = ",val 
				cur.execute('update airport2_perm set tickets = %s where from_loc = %s and to_loc = %s and date_ = %s', (val,dict['from'],dict['to'],dict['Date']))
				db.commit()
				cur.execute('select tickets,cost from airport2_perm where from_loc = %s and to_loc = %s and date_ = %s',(dict['from'],dict['to'],dict['Date']))
				for row1 in cur.fetchall():
					print row1
				inputs.remove(s)
				outputs.append(s)

				message_queue[s].put(dicte)	
				print "\n\n----------------- Type5 ended ---------------"


			else :

				print("Ignore these messages ")
 
			# s.close()		
	# Handle outputs
	for s in writable:
		print "\n\n++++++++++ Inside writable ++++++++++"
		try:
			dict = message_queue[s].get_nowait()
		except Queue.Empty:
			# No messages waiting so stop checking for writability.
			#print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
			outputs.remove(s)
		else:
			
			#print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
			#now we need to send the message to respective connection
			# print "inside writable"
			print dict
			server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server.connect((server_ip,server_host))
			print "send to the central server"
			dicte =  json.dumps(dict).encode('utf-8')
			server.send(dicte)
			#server.close()

			# f.write("Sending message now to connection " + str(s) + "\n")
			s.close()

			outputs.remove(s)
		print "--------- Inside writable Ended -----------"

	# Handle "exceptional conditions"
	for s in exceptional:

		#print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
		# Stop listening for input on the connection
		inputs.remove(s)
		if s in outputs:
			outputs.remove(s)
		s.close()

		# Remove message queue
		del message_queue[s]





	# if(len(msg) ==0 ) :
	# 	continue

	# c is the connection , conn.recv will read as many bytes as possible
	# database will be queried and message will be sent 

	# send a thank you message to the client. 
	# c.send('Thank you for connecting')
 
	# Close the connection with the client
	# c.close()

	# print(" You want to continue or not ") 
	

