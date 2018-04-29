# first of all import the socket library
import socket	
import json		   
import time
import logging
import select
import Queue
import copy

# change id 
# change port
# change data['id']
id = 1

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

# ip = '0.0.0.0'
# port1 = 10000
# server_add = ('0.0.0.0',10000)

ips =  {}
ips['airport1'] = ['0.0.0.0',10000]
ips['airport2'] = ['0.0.0.0',10001]
ips['hotel'] = ['0.0.0.0',10002]
ips['heartbeat'] = ['0.0.0.0',10003]


#airport1.connect(ips['airport1'])
#airport2.connect(ips['airport2'])
#hotel.connect(ips['hotel'])
#heartbeat.connect(ips['heartbeat'])

timeout = 60

print("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 1245 but it can be anything
port = 12559		
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
server.bind(('0.0.0.0',port))		
print("socket binded to %s" %(port))
 
# put the socket into listening mode
server.listen(5)	 
print("socket is listening")		  
 
# a forever loop until we interrupt it or 
# an error occurs
start_time = time.time()

requests_list = {}

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
message_queue = {}
message_queue[airport1] = Queue.Queue()
message_queue[airport2] = Queue.Queue()
message_queue[hotel] = Queue.Queue()
counter = int(0)

print "opening logs.txt"
f = open("logs.txt",'a')

while True:

	# Establish connection with client.
	readable, writable, exceptional = select.select(inputs, outputs, inputs)

	# Handle inputs
	for s in readable:

		if s is server:
			print "\n\n =========== SERVER listening ================="
			# A "readable" server socket is ready to accept a connection
			connection, client_address = s.accept()
			print "recieved connection from ",client_address
			# print "socket made for the client = ",connection.getsockname()
			#print >>sys.stderr, 'new connection from', client_address
			connection.setblocking(0)
			inputs.append(connection)
			# print "inputs"
			# print(inputs)
			# Give the connection a queue for data we want to send
			message_queue[connection] = Queue.Queue()
			f.write("Got Connection from "+str(client_address) + "\n")


			# heartbeat case 
			# dicte = {}
			# dicte['sender'] = 'central'
			# dicte['flag'] = 'log'
			# dicte['msg'] = "Got connection from "+str(connection) 
			# outputs.append(heartbeat)
			# message_queue[heartbeat].append(dicte)
			print "=========== SERVER part over ================="

		else:
			# print "client socket = ",s
			data = s.recv(1024)
			# print data

			if data:

				# A readable client socket has data
				#print >>sys.stderr, 'received "%s" from %s' % (data, s.getpeername())
				dict = json.loads(data.decode('utf-8'))
				# print dict
				#message_queue[s].put(dict)
				# Add output channel for response
				if dict['sender'] == 'heartbeat' :
					inputs.remove(s)
					outputs.append(s)
					dicte = {}
					dicte['flag'] = 'alive' # 1 is requests_list update , 2 is log update , 3 is zinda hain bolne wala update
					message_queue[s].put(dicte)
					continue

				elif dict['sender'] == 'client' :

					from_ = dict['from']
					to_ = dict['to']
					# print from_,to_
					if (from_,to_) in graph : 
						print "\n\n-------------------client 1 HOP started --------------------"

						
						# direct flight exists ,check if the flag is read ,
						#if it is read , just get the data from permanent store from airport server 
						dicte = {}
						if graph[ (from_,to_) ] == 'airport1' :
							# send message to airport 1 and hotel
							# Create a socket object

							# airport1.connect(ips[airport1])
							# hotel.connect(ips[hotel])
							# print("reached here in airport one")
							# outputs.append(airport1)
							# outputs.append(hotel)
							host = airport1
							dicte['pos'] = 1
							dicte['pose'] =1

						
						else :
						# 	outputs.append(airport2)
						# 	outputs.append(hotel)
							host = airport2
							dicte['pos'] = 2
							dicte['pose'] = 2
						
						
						dicte['from'] = from_
						dicte['to'] = to_
						dicte['Date'] = dict['date']
						dicte['sender'] = 'central'
						dicte['index'] = counter
						dicte['id'] =1 

						dicte[ int(dicte['pos']) ] = -1
						dicte['hops'] = 1
						dicte['people'] = dict['people']
						if dict['type'] == 1 :
							# read type 
							dicte['type'] = 1 # read from permanent
						else :
							dicte['type'] = 2 # write permanent value , since it is not a write type 
							# 3 is undo permanent value 
							
						dicte['budget'] = dict['budget']
						dicte['timer'] = time.time() # this is used when we want to delete a request that has crossed certain limit .
						# print "host",host


						dicte['ip'] = s.getsockname()[0]
						dicte['port'] =s.getsockname()[1]

						# dicte['client_ip'] = dict['client_ip']
						# dicte['client_port'] = dict['client_port']

						# print("pos = " + str(dicte['pos']))
						outputs.append(host)
						message_queue[host].put(dicte)

						dicte['pos'] = 3
						dicte[3] = -1


						outputs.append(hotel)
						message_queue[hotel].put(dicte)

						# dicte['flag'] = 'insert'
						# outputs.append(heartbeat)
						# message_queue[heartbeat].append(dicte)
						print "\n------------------"
						print "client(socket) - ",s
						print "------------------"
						dicte['conn'] = s
						dicte['valid'] = 1 # else it would be invalid , if we delete this entry 
						# print "c = ", counter
						temp = copy.deepcopy(dicte)
						temp['conn'] = s
						temp['cost'] = int(0)
						requests_list[counter] = temp

						# print "printing the requests_list"
						# a1_sorted_keys = sorted(requests_list[counter], key=requests_list[counter].get, reverse=False)
						# for i in a1_sorted_keys:
						# 	print i, "\t = ",requests_list[counter][i]

						dicte.pop('conn',None)
						f.write("Added message in logs "+str(from_)+" "+str(to_) + "\n")
						
						dicte['flag'] = 'request'

						# print "\nprinting the final client dict"
						# dicte_sorted_keys = sorted(dicte, key=dicte.get, reverse=False)
						# for i in dicte_sorted_keys:
						# 	print i, "\t = ",dicte[i]
						
						# outputs.append(heartbeat)
						# message_queue[heartbeat].append(dicte)

						# print "\n \n printing the requests_list"
						# a1_sorted_keys = sorted(requests_list[counter], key=requests_list[counter].get, reverse=False)
						# for i in a1_sorted_keys:
						# 	print i, "\t = ",requests_list[counter][i]
						inputs.remove(s)
						print "-----------------client 1 HOP finished --------------------------"

					else : 
						print "-----------------client 2 HOP started --------------------------"
						# this is a 1 hop message , needs to be verified in both the sides 
						flag = False
						for i in locations: 
							
							if i!=from_ and i != to_ and (from_,i) in graph and (i,to_) in graph :

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
							message_queue[s].put(dicte)
							
							f.write("Cannot find path from "+str(from_)+"  to "+str(to_) + "\n")
							dicte['flag'] = 'log'
							# outputs.append(heartbeat)
							# message_queue[heartbeat].append(dicte)
	
							continue


						dicte = {}
						dicte['from'] = from_
						dicte['to'] = i
						dicte['Date'] = dict['date']
						dicte['sender'] = 'central'
						dicte['index'] = counter
						dicte['pos'] = 1
						dicte['id'] = 1

						dicte[1] = -1
						dicte[2] = -1
						dicte[3] = -1

						dicte['hops'] = 2
						dicte['people'] = dict['people']
						if dict['type'] == 1 :
							# read type 
							dicte['type'] = 1 # read from permanent
						else :
							dicte['type'] = 2 # write temp value , since it is not a write type 

						dicte['budget'] = dict['budget']
						dicte['timer'] = time.time() # this is used when we	
						

						dicte['ip'] = s.getsockname()[0]
						dicte['port'] =s.getsockname()[1]


						# dicte['flag'] = dict['flag']
						t_a1 = copy.deepcopy(dicte)
						message_queue[airport1].put(t_a1)

						dicte['pos']= 2
						dicte['from']= i
						dicte['to'] = to_

						dicte[1] = -1
						dicte[2] = -1
						dicte[3] = -1
						t_a2 = copy.deepcopy(dicte)
						message_queue[airport2].put(t_a2)

						dicte['pos'] = 3
						t_a3 = copy.deepcopy(dicte)
						message_queue[hotel].put(t_a3)
						
						dicte['from'] = from_
						dicte['to'] = to_
						dicte['inter'] = i
						dicte['processed'] = 0
						dicte['conn'] = s


						temp = copy.deepcopy(dicte)
						temp['conn'] = s
						temp['cost'] = int(0)
						requests_list[counter] = temp

						dicte.pop('conn',None)

						dicte['flag'] = 'insert'
						# message_queue[heartbeat].append(dicte)
						dicte['flag'] = 'request'

						f.write("Added message "+str(from_)+"  to "+str(to_)+" to message_queue" + "\n")
						
 
						outputs.append(hotel)
						outputs.append(airport1)
						outputs.append(airport2)
						# outputs.append(heartbeat)
						# outputs.append(heartbeat)
						print "-----------------client 2 HOP ended --------------------------"

					counter = counter + 1

				else : 

					#if s in [airport1,airport2,hotel] :
					if dict['sender'] in ['airport_1','airport_2','hotel']:
						print "\n\n+++++++++++++++++++++++++++++++++++++++++++++++++"

					print "msg from airport1, hotel , airport2 -----------------------"
					# the sender is aiport1  or airport2 or hotel
					# print(type(dict))
					idx = dict['index']
					pos = dict['pos']

				

					if idx in requests_list and dict['id'] == id:
						print("pos = " + str(pos)+ "\tidx = "+str(dict['flag'])+ "\tidx =" +str(dict['type']))
						if dict['type'] == 4 or dict['type'] == 5 or dict['type']== -2 : 
							#if ticket is booked or not
							requests_list[idx][pos] = -2
						else :
							# print(str(dict['flag'])+" is used heree")
							requests_list[idx][pos] = dict['flag']
							requests_list[idx]['cost']+= int(dict['cost'])
							requests_list[idx]['type'] =  dict['type']

						s.close()
						inputs.remove(s)


					else : 
						
						# this index dict has been removed due to timeout . so send undo message to the particular connection s
						
						if dict['type'] == 2:
							# it is update of temporary , so we send undo message with 
							dict['type'] = 4
							inputs.remove(s)
							outputs.append(s)
							message_queue[s].put(dict)

						elif dict['type'] == 3:

							dict['type'] = 5
							inputs.remove(s)
							outputs.append(s)
							message_queue[s].put(dict)

						else :

							dict[1] = -2 
							dict[2]  = -2
							dict[3] = -2
							# this is already a undo operation .airport has already done that , so 
							# we dont have to care about them and we'll ignore this message .
							
							print('Add this to commit log info')
							inputs.remove(s)

					print "--------------Database Finished-----------------------"		
						# elif dicte['type'] == 3  : -> TODO
						#	dicte['type'] = 5 
						#	inputs.remove(s)
						#	outputs.append(s)
						#	message_queue[s].append(dicte)

			else:

				# Interpret empty result as closed connection
				#print >>sys.stderr, 'closing', client_address, 'after reading no data'
				# Stop listening for input on the connection
				if s in outputs:
					outputs.remove(s)
				inputs.remove(s)
				s.close()

				# Remove message queue
				del message_queue[s]



	# Handle outputs
	for s in writable:
		print "\n\n----------- inside writable ------------"
		try:
			dict = message_queue[s].get_nowait()
			print dict
			print "------------------------------"
		except Queue.Empty:
			# No messages waiting so stop checking for writability.
			#print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
			outputs.remove(s)
		else:
			
			#print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
			#now we need to send the message to respective connection
			# print "inside writable"
			if s is airport1:
				print "airport_1" 
				airport1.connect((ips['airport1'][0],ips['airport1'][1]))
				# print dict
				dicte =  json.dumps(dict).encode('utf-8')
				s.send(dicte)
				print "send to the airport_1",(ips['airport1'][0],ips['airport1'][1])

				tvalue = message_queue[airport1]
				# del message_queue[airport1]
				airport1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				message_queue[airport1] = tvalue
				#s.close()
			elif s is airport2:
				print "airport_2"
				airport2.connect((ips['airport2'][0],ips['airport2'][1]))
				# print dict
				dicte =  json.dumps(dict).encode('utf-8')
				s.send(dicte)
				print "send to the airport_2",(ips['airport2'][0],ips['airport2'][1])

				tvalue = message_queue[airport2]
				# del message_queue[airport2]
				airport2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				message_queue[airport2] = tvalue

				#s.close()
			elif s is hotel:
				print "hotel"
				s.connect((ips['hotel'][0],ips['hotel'][1]))
				dicte =  json.dumps(dict).encode('utf-8')
				s.send(dicte)
				print "send to the hotel",(ips['hotel'][0],ips['hotel'][1])

				tvalue = message_queue[hotel]
				# del message_queue[hotel]
				hotel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				message_queue[hotel] = tvalue
				#s.close()
			else:
				# sending back to client
				# print "printing the port from which client talked",(dict['client_ip'],dict['client_port']) 
				# s.connect(dicte['client_ip'],dicte['client_port']) )
				print "sending back to client",s.getsockname()
				dicte =  json.dumps(dict).encode('utf-8')
				s.send(dicte)
				#s.close()	


			f.write("Sending message now to connection " + str(s.getsockname()) + "\n")
			outputs.remove(s)
		print "-------- end of inside writable --------------\n"
			


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



	# now we check the request queue if any of the message exceeded its timeout limit
	print "\n\n+++++++++ checking for removables ++++++++++ "
	removable = []
	for key in requests_list :

		# if it has timedout .
		tim = time.time()
		value  = requests_list[key]
		# print "dict values from the requests_list"
		# for i in value:
		# 	print i,("\t = "),value[i]
		# print "---------- dict printed -------- "

		print "\n --printing the requests_list----"
		a1_sorted_keys = sorted(value, key=value.get, reverse=False)
		for i in a1_sorted_keys:
			print i, "\t = ",value[i]
		print "---------- dict printed -------- "

		
		s1 = value['conn']
		v = tim - value['timer']
		# print "value['from'] = ",value['from'], " value[to] = ", value['to']
		print "tim - value['timer'] = ",v, " timeout = ", timeout
		if tim - value['timer'] > timeout:
			print "\n---------inside timeout --------"
			# wrong line need to give a tuple with ip and port
			
			# s1 = socket.socket()
			# s1.connect( (value['ip'],value['port']) )
			outputs.append(s1)

			value['result']= 3 # timeout
			value['message'] = "Timeout Happened"
			value.pop('conn',None)
			if s1 in message_queue :
				message_queue[s1].put(value)

			f.write("Message has been removed from list "+str(key)+" due to timeout" + "\n")
			removable.append(key)
			print "-------end timeout--------------"


		else :

			print " \n --------No timeout------"
			if value['hops'] == 1:
				print "\n--------------------1 HOP -------------------"
				print "value 1 = ", value[ int(value['pose']) ] , "\t value 3 = ", value[3]
				# 1 is for aiport1 and 3 is for hotel
				if value[ int(value['pose']) ] >0 and value[3] >0 : 

					# this is successful transaction
					# s1 = socket.socket()
					# s1.connect( (value['client_ip'],value['client_port']) )
					# print "socket ip,port",s.getsockname()
					# print "printing the port from which client talked",(value['client_ip'],value['client_port']) 
					value['result'] = 1 # 1 is successful

					# need to do 2 phase commit part
					if int(value['type'] ) == 2 :
						print( "\n------------------type2--------------------------")
						if int(value['cost']) < int(value['budget']) :	
							print "commit the changes"
							value['type'] = 3 
							
						else :
							print "abort the changes"
							value['type'] = 4

						temp = copy.deepcopy(value)
						temp.pop('conn',None)
						temp.pop('cost',None)

						if value['pose'] == 1:
							outputs.append(airport1)
							message_queue[airport1].put(temp)

						else :
							outputs.append(airport2)
							message_queue[airport2].put(temp)

						message_queue[hotel].put(temp)
						outputs.append(hotel)
						print( "------------------Ending type2--------------------------")
					

					elif int(value['type']) == 3:

						print( "\n------------------type3--------------------------")
						outputs.append(value['conn'])
						# print "Value = "
						# 	print value
						# 	print "outputs = "
						# 	print outputs 
						if s1 not in message_queue :
							message_queue[s1] = Queue.Queue()
							
						#s2 = value['conn']
						value.pop('conn',None)
						message_queue[s1].put(value)
						removable.append(key)
						print( "------------------Ending type3 --------------------------")


					elif int(value['type']) == 4 :

						value['result'] = 2
						value['answer'] = "Budget is too low and not possible to book"
						print( "\n------------------type4--------------------------")
						outputs.append(value['conn'])
						# print "Value = "
						# 	print value
						# 	print "outputs = "
						# 	print outputs 
						if s1 not in message_queue :
							message_queue[s1] = Queue.Queue()
							
						#s2 = value['conn']
						value.pop('conn',None)
						message_queue[s1].put(value)
						removable.append(key)
						print( "------------------Ending type4 --------------------------")



						# yes , so send back mesages to airport1 ,hotel to commit changes
					elif int(value['type']) == 1:

						print( "\n------------------type1--------------------------")
						if int(value['cost']) < int(value['budget']) :	
							print "sufficient budget"
						else :
							print("Yeah less budget")
							value['flag'] = -2
							value['result']  = 2
							value['answer'] = "Budget is too low and not possible to book"
						
						outputs.append(value['conn'])
						# print "Value = "
						# print value
						# print "outputs = "
						# print outputs 
						if s1 not in message_queue :
							message_queue[s1] = Queue.Queue()
						
						s2 = value['conn']
						value.pop('conn',None)
						message_queue[s1].put(value)
						removable.append(key)

						print( "------------------End type1--------------------------")
	
				elif value[ int(value['pose']) ] == -2 or value[3] == -2 :

					# one of them failed , 2 phase commit failed 
					# this is successful transaction
					# s1 = socket.socket()
					# s1.connect( (value['ip'],value['port']) )
					if value[int(value['pose'])] > 0:

						if int(value['type'] ) == 2 :
							print( "\n------------------type2/4--------------------------")
							# if int(value['cost']) < int(value['budget']) :	
							# 	value['type'] = 3 
							# 	print "commit the changes"
							# else :
							# 	print "abort the changes"
							# 	value['type'] = 4
							print "abort the changes"
							value['type'] = 4

							temp = copy.deepcopy(value)
							temp.pop('conn',None)
							temp.pop('cost',None)

							if value['pose'] == 1:
								outputs.append(airport1)
								message_queue[airport1].put(temp)

							else :
								outputs.append(airport2)
								message_queue[airport2].put(temp)
							print( "------------------Ending type2/4--------------------------")
							value[value['pose'] ] = -2

					if value[3] > 0:
						if int(value['type'] ) == 2 :
							print( "\n------------------type2/4--------------------------")
							print "abort the changes"
							value['type'] = 4

							temp = copy.deepcopy(value)
							temp.pop('conn',None)
							temp.pop('cost',None)

							outputs.append(hotel)
							message_queue[hotel].put(temp)
							print( "------------------Ending type2/4--------------------------")
							value[3] = -2

					count = int(0)
					if value[ value['pose'] ] == -2 :
						count = count +1
					if value[3] == -2 :
						count = count +1

					if count ==2 :
 						
 						value['result'] = 2 # 1 is un-successful
						outputs.append(value['conn'])
						if s1 not in message_queue :
							message_queue[s1] = Queue.Queue()

						s2 = value['conn']
						value.pop('conn',None)

						message_queue[s1].put(value)
						removable.append(key)


				print "--------------------1 HOP end-------------------"

			else:
				print "\n--------------------2 HOP start-------------------"

				print "value 1 = ", value[1] , "\t value 2 = ", value[2], "\t value 3 = ", value[3]
				if value[1] >0 and value[2]>0 and value[3] >0 : 
					value['result'] = 1
					# need to do 2 phase commit part
					if int(value['type'] ) == 2 :
						print( "\n------------------type2--------------------------")
						if int(value['cost']) < int(value['budget']) :	
							value['type'] = 3 
							print "commit the changes"
						else :
							print "abort the changes"
							value['type'] = 4

						temp = copy.deepcopy(value)
						temp.pop('conn',None)
						temp.pop('cost',None)

						a1 = copy.deepcopy(temp)
						a1['to'] = a1['inter']
						outputs.append(airport1)
						message_queue[airport1].put(a1)

						a2 = copy.deepcopy(temp)
						a2['from'] = a2['inter']
						outputs.append(airport2)
						message_queue[airport2].put(a2)
						
						message_queue[hotel].put(temp)
						outputs.append(hotel)


						print( "------------------Ending type2--------------------------")
					

					elif int(value['type']) == 3 :

						print( "\n------------------type3--------------------------")
						outputs.append(value['conn'])
						# print "Value = "
						# 	print value
						# 	print "outputs = "
						# 	print outputs 
						if s1 not in message_queue :
							message_queue[s1] = Queue.Queue()
							
						#s2 = value['conn']
						value.pop('conn',None)
						message_queue[s1].put(value)
						removable.append(key)
						print( "------------------Ending type3 --------------------------")


					elif int(value['type']) == 4 :

						value['result'] = 2
						value['answer'] = "Budget is too low and not possible to book"
						print( "\n------------------type4--------------------------")
						outputs.append(value['conn'])
						# print "Value = "
						# 	print value
						# 	print "outputs = "
						# 	print outputs 
						if s1 not in message_queue :
							message_queue[s1] = Queue.Queue()
							
						#s2 = value['conn']
						value.pop('conn',None)
						message_queue[s1].put(value)
						removable.append(key)
						print( "------------------Ending type4 --------------------------")

						# yes , so send back mesages to airport1 ,hotel to commit changes
					elif int(value['type']) == 1:

						print( "\n------------------type1--------------------------")
						if int(value['cost']) < int(value['budget']) :	
							print "sufficient budget"
						else :
							print("Yeah less budget")
							value['flag'] = -2 
							value['result']	= 2
							value['answer'] = "Budget is too low and not possible to book"
						
						outputs.append(value['conn'])
						# print "Value = "
						# print value
						# print "outputs = "
						# print outputs 
						if s1 not in message_queue :
							message_queue[s1] = Queue.Queue()
						
						s2 = value['conn']
						value.pop('conn',None)
						message_queue[s1].put(value)
						removable.append(key)

						print( "------------------End type1--------------------------")

				elif value[1] == -2 or value[3] == -2 or value[2]== -2 :
					print "entered here"
					if value[1] > 0:
						if int(value['type'] ) == 2 :
							print( "\n------------------type2/4--------------------------")
							# if int(value['cost']) < int(value['budget']) :	
							# 	value['type'] = 3 
							# 	print "commit the changes"
							# else :
							# 	print "abort the changes"
							# 	value['type'] = 4
							print "abort the changes"
							value['type'] = 4
							temp = copy.deepcopy(value)
							temp.pop('conn',None)
							temp.pop('cost',None)

							a1 = copy.deepcopy(temp)
							a1['to'] = a1['inter']
							outputs.append(airport1)
							message_queue[airport1].put(a1)
							print( "------------------Ending type2/4--------------------------")
							value[1] =-2

					if value[2] > 0:
						if int(value['type'] ) == 2 :
							print( "\n------------------type2/4--------------------------")
							# if int(value['cost']) < int(value['budget']) :	
							# 	value['type'] = 3 
							# 	print "commit the changes"
							# else :
							# 	print "abort the changes"
							# 	value['type'] = 4
							print "abort the changes"
							value['type'] = 4
							temp = copy.deepcopy(value)
							temp.pop('conn',None)
							temp.pop('cost',None)

							a2 = copy.deepcopy(temp)
							a2['from'] = a2['inter']
							outputs.append(airport2)
							message_queue[airport2].put(a2)
							print( "------------------Ending type2/4--------------------------")
							value[2] = -2

					if value[3] > 0:
						print "qwerty"
						if int(value['type'] ) == 2 :
							print( "\n------------------type2/4--------------------------")
							# if int(value['cost']) < int(value['budget']) :	
							# 	value['type'] = 3 
							# 	print "commit the changes"
							# else :
							# 	print "abort the changes"
							# 	value['type'] = 4
							print "abort the changes"
							value['type'] = 4
							temp = copy.deepcopy(value)
							temp.pop('conn',None)
							temp.pop('cost',None)

							outputs.append(hotel)
							message_queue[hotel].put(temp)
							print( "------------------Ending type2/4--------------------------")
							value[3] = -2


					count = int(0)
					if value[1] == -2 :
						count = count +1

					if value[2] == -2 :
						count = count +1

					if value[3] == -2 :
						count = count +1

					
					if count == 3 :
						# one of them failed , 2 phase commit failed 
						#sending back result to the client
						value['result'] = 2 # 1 is un-successful
						outputs.append(s1)
						if s1 not in message_queue :
							message_queue[s1] = Queue.Queue()

						value.pop('conn',None)
						message_queue[s1].put(value)
						removable.append(key)

				print "--------------------2 HOP end-----------------------"

	for i in removable :
		requests_list.pop(i,None)

	print "-------- end of checking for removables ---------"



