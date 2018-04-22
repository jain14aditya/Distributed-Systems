# first of all import the socket library
import socket	
import json		   
import time
import logging
import select


# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

airport1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#airport1.setblocking(0)

airport2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#airport2.setblocking(0)

hotel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#hotel.setblocking(0)


heartbeat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#heartbeat.setblocking(0)


ips =  {}
ips['airport1'] = ('192.168.0.11',10000)
ips['airport2'] = ('192.168.0.11',10001)
ips['hotel'] = ('192.168.0.11',10002)
ips['heartbeat'] = ('192.168.0.11',10003)


airport1.connect(ips['airport1'])
airport2.connect(ips['airport2'])
hotel.connect(ips['hotel'])
heartbeat.connect(ips['heartbeat'])


timeout_message = 60

print("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 1245 but it can be anything
port = 12559			
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
server.bind(('192.168.0.11',port))		
print("socket binded to %s" %(port))
 
# put the socket into listening mode
server.listen(5)	 
print("socket is listening")		  
 
# a forever loop until we interrupt it or 
# an error occurs
start_time = time.time()

requests_list = []

graph = {}
graph[ ('A','B') ] = 'airport1'
graph[ ('C','B') ] = 'airport1'
graph[ ('D','B') ] = 'airport1'
graph[ ('C','D') ] = 'airport1'


graph[ ('B','A') ] = 'airport2'
graph[ ('B','C') ] = 'airport2'
graph[ ('B','D') ] = 'airport2'

locations = ['A','B','C','D']


inputs = [server]
outputs = []
message_queues = {}

counter = int(0)

f = open("logs.txt",'a')


while True:

	# Establish connection with client.
	readable, writable, exceptional = select.select(inputs, outputs, inputs)

	# Handle inputs
	for s in readable:

		if s is server:
			
			# A "readable" server socket is ready to accept a connection
			connection, client_address = s.accept()
			#print >>sys.stderr, 'new connection from', client_address
			connection.setblocking(0)
			inputs.append(connection)

			# Give the connection a queue for data we want to send
			message_queue[connection] = Queue.Queue()
			f.write("Got Connection from "+str(connection))
			dicte = {}
			dicte['sender'] = 'central'
			dicte['flag'] = 'log'
			dicte['msg'] = "Got connection from "+str(connection) 
			outputs.append(heartbeat)
			message_queue[heartbeat].append(dicte)


		else:

			data = s.recv(1024)

			if data:

				# A readable client socket has data
				#print >>sys.stderr, 'received "%s" from %s' % (data, s.getpeername())
				dict = json.loads(data.decode('utf-8'))
				#message_queues[s].put(dict)
				# Add output channel for response
				if dict['sender'] == 'heartbeat' :
					inputs.remove(s)
					outputs.append(s)
					dicte = {}
					dicte['flag'] = 3 # 1 is request_list update , 2 is log update , 3 is zinda hain bolne wala update
					message_queue[s].append(dicte)

				elif dict['sender'] == 'client' :

					from_ = dict['from']
					to_ = dict['to']

					if (from_,to_) in graph : 
						
						# direct flight exists ,check if the flag is read ,
						#if it is read , just get the data from permanent store from airport server 
						if graph[ (from_,to_) ] == 1 :
							# send message to airport 1 and hotel
							# Create a socket object
							outputs.append(airport1)
							outputs.append(hotel)
							host = airport1

						else :
							outputs.append(airport2)
							outputs.append(hotel)
							host = airport2

						
						dicte = {}
						dicte['from'] = from_
						dicte['to'] = to_
						dicte['Date'] = dict['date']
						dicte['sender'] = 'central'
						dicte['index'] = counter
						dicte['pos'] = '1'
						dicte['1'] = -1
						dicte['hops'] = 1
						dicte['people'] = dict['people']
						if dict['type'] == 1 :
							# read type 
							dicte['type'] = 0 # read from permanent
						else :
							dicte['type'] = 2 # write permanent value , since it is not a write type 
							# 3 is undo permanent value 
							
						dicte['budget'] = dict['budget']
						dicte['timer'] = time.time() # this is used when we want to delete a request that has crossed certain limit .

						message_queue[host].append(dicte)

						dicte['pos'] = '3'
						dicte['3'] = -1

						message_queue[hotel].append(dicte)

						dicte['flag'] = 'insert'
						outputs.append(heartbeat)
						message_queues[heartbeat].append(dicte)

						dicte['conn'] = s

						dicte['valid'] = 1 # else it would be invalid , if we delete this entry 

						requests_list[counter] = dicte
						f.write("Added message in logs "+str(from_)+" "+str(to_))
						
						dicte['flag'] = 'request'
						outputs.append(heartbeat)
						message_queue[heartbeat].append(dicte)

					else : 

						# this is a 1 hop message , needs to be verified in both the sides 
						flag = False
						for i in locations: 
							
							if i!=from_ and i != to_ and (from_,i) in graph_ and (i,to_) in graph :

								#two hop message , take the one path and query it .
								#todo - >  can also add minimum cost path to consideration
								flag = True
								break


						if flag == False :

							# no flight exists in 1 hop 
							outputs.append(s)
							inputs.remove(s)
							dicte = {}
							dicte['sender'] = 'central'
							dicte['flag'] = '0'
							dicte['cost'] = 0
							message_queues[s].append(dicte)
							
							f.write("Cannot find path from "+str(from_)+"  to "+str(to_))
							dicte['flag'] = 'log'
							outputs.append(heartbeat)
							message_queue[heartbeat].append(dicte)
	
							continue


						dicte = {}
						dicte['from'] = from_
						dicte['to'] = i
						dicte['Date'] = dict['date']
						dicte['sender'] = 'central'
						dicte['index'] = counter
						dicte['pos'] = '1'
						dicte['hops'] = 1
						dicte['people'] = dict['people']
						if dict['type'] == 1 :
							# read type 
							dicte['type'] = 0 # read from permanent
						else :
							dicte['type'] = 2 # write temp value , since it is not a write type 

						dicte['budget'] = dict['budget']
						dicte[timer] = time.time() # this is used when we	
						message_queues[airport1].append(dicte)

						dicte['pos']= '2'
						dicte['from']= i
						dicte['to'] = to_
						dicte['1'] = -1
						dicte['2'] = -1
						dicte['3'] = -1

						message_queues[airport2].append(dicte)

						dicte['pos'] = '3'

						message_queues[hotel].append(dicte)
						
						dicte['from'] = from_
						dicte['to'] = to_
						dicte['inter'] = i
						dicte['processed'] = 0
						dicte['conn'] = s


						requests_list[counter] = dicte
						dicte['flag'] = 'insert'
						message_queues[heartbeat].append(dicte)
						dicte['flag'] = 'request'

						f.write("Added message "+str(from_)+"  to "+str(to_)+" to message_queue")
						
 
						outputs.apppend(hotel)
						outputs.append(airport1)
						outputs.append(airport2)
						outputs.append(heartbeat)
						outputs.append(heartbeat)

					counter = counter + 1


				else : 

					# the sender is aiport1  or airport2 or hotel
					idx = dicte['index']
					pos = dicte['pos']

					if idx in request_list :
						#if ticket is booked or not
						request_list[idx][pos] = dicte['flag'] 
						inputs.remove(s)

					else : 
						
						# this index dict has been removed due to timeout . so send undo message to the particular connection s
						if dicte['type'] == 1 :
							# it is a read message ,so no need to send undo operation 
							# since we already sent a message to client due to timeout , we dont have to care about this
							print("Common")
							inputs.remove(s)

						elif dicte['type'] == 2:
							# it is update of temporary , so we send undo message with 
							dicte['type'] = 4
							inputs.remove(s)
							outputs.append(s)
							message_queues[s].append(dicte)

						elif dicte['type'] == 4:
							# this is already a undo operation .airport has already done that , so 
							# we dont have to care about them and we'll ignore this message .
							print('Add this to commit log info')
							inputs.remove(s)


						# elif dicte['type'] == 3  : -> TODO
						#	dicte['type'] = 5 
						#	inputs.remove(s)
						#	outputs.append(s)
						#	message_queues[s].append(dicte)

			else:

				# Interpret empty result as closed connection
				#print >>sys.stderr, 'closing', client_address, 'after reading no data'
				# Stop listening for input on the connection
				if s in outputs:
					outputs.remove(s)
				inputs.remove(s)
				s.close()

				# Remove message queue
				del message_queues[s]



	# Handle outputs
	for s in writable:

		try:
			dict = message_queues[s].get_nowait()
		except Queue.Empty:
			# No messages waiting so stop checking for writability.
			#print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
			outputs.remove(s)
		else:
			
			#print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
			#now we need to send the message to respective connection
			s.send(dict)
			f.write("Sending message now to connection " + str(s))
			outputs.remove(s)

			


	# Handle "exceptional conditions"
	for s in exceptional:

		#print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
		# Stop listening for input on the connection
		inputs.remove(s)
		if s in outputs:
			outputs.remove(s)
		s.close()

		# Remove message queue
		del message_queues[s]



	# now we check the request queue if any of the message exceeded its timeout limit

	removable = []

	for key in request_list :

		# if it has timedout .
		tim = time.time()
		value  = request_list[key]

		if tim - value['time'] > timeout  :

			socket = socket.socket()
			socket.connect(value['conn'])
			output.append(socket)

			value['result']= 3 # timeout 
			if socket in message_queues :
				message_queues[socket].append(value)

			f.write("Message has been removed from list "+str(key)+" due to timeout")
			removable.append(key)

		else :

			if value['hops'] == 1:

				# 1 is for aiport1 and 3 is for hotel
				if value['1'] >0 and value['3'] >0 : 

					# this is successful transaction
					socket = socket.socket()
					socket.connect(value['conn'])
					value['result'] = 1 # 1 is successful
					outputs.append(socket)
					message_queue[socket].append(value)


				elif value['1'] == -2 or value['3'] == -2 :

					# one of them failed , 2 phase commit failed 
					# this is successful transaction
					socket = socket.socket()
					socket.connect(value['conn'])
					value['result'] = 2 # 1 is un-successful
					outputs.append(socket)
					message_queue[socket].append(value)
					removable.append(key)


			else :

				if value['1'] >0 and value['2']>0 and value['3'] >0 : 

					# this is successful transaction
					socket = socket.socket()
					socket.connect(value['conn'])
					value['result'] = 1 # 1 is successful
					outputs.append(socket)
					message_queue[socket].append(value)


				elif value['1'] == -2 or value['3'] == -2 or value['2']== -2 :

					# one of them failed , 2 phase commit failed 
					socket = socket.socket()
					socket.connect(value['conn'])
					value['result'] = 2 # 1 is successful
					outputs.append(socket)
					message_queue[socket].append(value)
					removable.append(key)


	for i in removable :
		request_list.remove(i)





