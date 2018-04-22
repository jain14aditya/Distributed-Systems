###### This is for the main server gui code , 

import tkinter
import socket
from tkinter import *
from tkinter import simpledialog
from tkinter.ttk import *
import calendar


# import tkinter.messagebox
# import ttkcalender
# import tkSimpleDialog.Dialog


def helloCallBack() :
	# here we need to take a message and parse it back to the central server
	# Create a socket object
	s = socket.socket()         
 
	# Define the port on which you want to connect
	port = 12558              


	# connect to the server on local computer
	s.connect(('10.145.236.136', port))


	#"" here we access database ""
	db = MySQLdb.connect("localhost","root","yoyo","distributed_systems")
	cursor = db.cursor()

	cursor.execute("select * from cent_message where from_loc='chennai';")

	# get a row
	data = cursor.fetchone()

	dic = {'a':data[0],'b':data[1],'index':data[2],'pos':data[3]}
	dict =  json.dumps(dic).encode('utf-8')
	
	s.sendall(dict)




def main() :

	top = tkinter.Tk()
	top.geometry("800x600+0+0")

	# use a colorful frame
	frame = tkinter.Frame(top, bg='green')
	frame.pack(fill='both', expand='yes')

	
	labelTo = Label(frame,width=10,text = "From",relief = RAISED)
	labelTo.place(x=100,y=300)

	labelFrom = Label(frame,width=10,text="To",relief = RAISED)
	labelFrom.place(x=100,y=400)


	variable = StringVar(frame)
	variable.set("A")

	variable2 = StringVar(frame)
	variable2.set("B")

	DropBoxTo = OptionMenu(frame,variable,"A","B","C","D")
	DropBoxTo.place(x=200,y=300)


	DropBoxFrom = OptionMenu(frame,variable2,"A","B","C","D")
	DropBoxFrom.place(x=200,y=400)

	L1 = Label(frame, text="Budget")
	L1.place(x=100,y=500)

	E1 = Entry(frame,width =10)
	E1.place(x=200,y=500)


	checkButton = tkinter.Button(frame,text ="Check Availability",command = helloCallBack,bg= 'yellow')
	checkButton.place(x=100,y=500)
	
	BookButton = tkinter.Button(frame,text ="Book Availability",command = helloCallBack,bg='yellow')
	BookButton.place(x=300,y=500)

	top.mainloop()



if __name__ == "__main__":
	main()