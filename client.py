# Import socket module
import socket               
import json
import MySQLdb

# Create a socket object
s = socket.socket()         
 
# Define the port on which you want to connect
port = 12558            
host = '10.17.12.27'

# connect to the server on local computer
s.connect((host, port))


#"" here we access database ""
db = MySQLdb.connect("localhost","root","yoyo","distributed_systems")
cursor = db.cursor()

cursor.execute("select * from cent_message where from_loc='chennai';")

# get a row
data = cursor.fetchone()

dic = {'a':data[0],'b':data[1],'index':data[2],'pos':data[3]}
dict =  json.dumps(dic).encode('utf-8')
s.sendall(dict)


 
# receive data from the server
a = s.recv(1024).decode("utf-8")
print(str(a) )
# close the connection
s.close()       

